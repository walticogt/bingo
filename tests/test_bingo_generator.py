"""
Tests para el generador de cartones de bingo
"""

import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bingo_generator import (
    generate_bingo_numbers,
    calculate_card_dimensions,
    calculate_card_positions,
    generate_pdf,
    COLUMN_RANGES,
    NUMBERS_PER_COLUMN
)


class TestBingoNumberGeneration(unittest.TestCase):
    """Tests para la generación de números de bingo"""

    def test_generate_bingo_numbers_structure(self):
        """Verifica que se generen números con la estructura correcta"""
        numbers = generate_bingo_numbers()

        # Verificar que tiene las 5 columnas
        self.assertEqual(len(numbers), 5)
        self.assertIn("B", numbers)
        self.assertIn("I", numbers)
        self.assertIn("N", numbers)
        self.assertIn("G", numbers)
        self.assertIn("O", numbers)

        # Verificar que cada columna tiene 5 elementos
        for letter in ["B", "I", "N", "G", "O"]:
            self.assertEqual(len(numbers[letter]), NUMBERS_PER_COLUMN)

    def test_generate_bingo_numbers_ranges(self):
        """Verifica que los números estén en los rangos correctos"""
        numbers = generate_bingo_numbers()

        for letter, (start, end) in COLUMN_RANGES.items():
            for num in numbers[letter]:
                # El centro puede ser texto
                if isinstance(num, int):
                    self.assertGreaterEqual(num, start)
                    self.assertLess(num, end)

    def test_generate_bingo_numbers_free_text(self):
        """Verifica que el texto libre se coloque en el centro"""
        free_text = "TEST"
        numbers = generate_bingo_numbers(free_text)

        # La columna N, posición 2 (centro) debe tener el texto libre
        self.assertEqual(numbers["N"][2], free_text)

    def test_generate_bingo_numbers_uniqueness(self):
        """Verifica que no haya números duplicados en una columna"""
        numbers = generate_bingo_numbers()

        for letter in ["B", "I", "G", "O"]:  # Excluir N porque tiene texto
            column_numbers = [n for n in numbers[letter] if isinstance(n, int)]
            self.assertEqual(len(column_numbers), len(set(column_numbers)))


class TestCardDimensions(unittest.TestCase):
    """Tests para el cálculo de dimensiones de cartones"""

    def test_calculate_card_dimensions_3x2(self):
        """Verifica el cálculo de dimensiones para layout 3×2"""
        page_width, page_height = 842, 595  # A4 landscape
        cards_per_row = 3
        cards_per_column = 2

        card_width, card_height = calculate_card_dimensions(
            page_width, page_height, cards_per_row, cards_per_column
        )

        self.assertGreater(card_width, 0)
        self.assertGreater(card_height, 0)
        self.assertIsInstance(card_width, float)
        self.assertIsInstance(card_height, float)

    def test_calculate_card_positions_3x2(self):
        """Verifica el cálculo de posiciones para 6 cartones"""
        page_width, page_height = 842, 595
        cards_per_row = 3
        cards_per_column = 2
        card_width, card_height = 250, 200

        positions = calculate_card_positions(
            page_width, page_height, cards_per_row, cards_per_column,
            card_width, card_height
        )

        # Debe haber 6 posiciones (3×2)
        self.assertEqual(len(positions), 6)

        # Todas las posiciones deben ser tuplas de 2 elementos
        for pos in positions:
            self.assertIsInstance(pos, tuple)
            self.assertEqual(len(pos), 2)


class TestPDFGeneration(unittest.TestCase):
    """Tests para la generación de PDFs"""

    def setUp(self):
        """Configuración antes de cada test"""
        self.test_output_dir = "tests/test_output"
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        """Limpieza después de cada test"""
        # Limpiar archivos de prueba
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                file_path = os.path.join(self.test_output_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.test_output_dir)

    def test_generate_pdf_basic(self):
        """Test básico de generación de PDF"""
        output_file = os.path.join(self.test_output_dir, "test_basic.pdf")

        result = generate_pdf(
            output_file=output_file,
            num_pages=1,
            cards_per_page=6
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_cards"], 6)
        self.assertEqual(result["total_pages"], 1)
        self.assertTrue(os.path.exists(output_file))

    def test_generate_pdf_multiple_pages(self):
        """Test de generación de múltiples páginas"""
        output_file = os.path.join(self.test_output_dir, "test_multiple.pdf")

        result = generate_pdf(
            output_file=output_file,
            num_pages=3,
            cards_per_page=6
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_cards"], 18)  # 3 páginas × 6 cartones
        self.assertEqual(result["total_pages"], 3)
        self.assertTrue(os.path.exists(output_file))

    def test_generate_pdf_with_export(self):
        """Test de generación con exportación de números"""
        output_file = os.path.join(self.test_output_dir, "test_export.pdf")

        result = generate_pdf(
            output_file=output_file,
            num_pages=1,
            cards_per_page=6,
            export_numbers=True
        )

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["json_file"])
        self.assertTrue(os.path.exists(result["json_file"]))

        # Verificar contenido del JSON
        with open(result["json_file"], 'r') as f:
            data = json.load(f)
            self.assertEqual(data["total_cards"], 6)
            self.assertEqual(len(data["cards"]), 6)

    def test_generate_pdf_custom_free_text(self):
        """Test con texto libre personalizado"""
        output_file = os.path.join(self.test_output_dir, "test_custom.pdf")
        custom_text = "GRATIS"

        result = generate_pdf(
            output_file=output_file,
            num_pages=1,
            cards_per_page=6,
            free_text=custom_text,
            export_numbers=True
        )

        self.assertTrue(result["success"])

        # Verificar que el JSON contiene el texto personalizado
        with open(result["json_file"], 'r') as f:
            data = json.load(f)
            self.assertEqual(data["free_text"], custom_text)

    def test_generate_pdf_invalid_pages(self):
        """Test con número de páginas inválido"""
        output_file = os.path.join(self.test_output_dir, "test_invalid.pdf")

        with self.assertRaises(ValueError):
            generate_pdf(
                output_file=output_file,
                num_pages=0
            )

    def test_generate_pdf_invalid_cards_per_page(self):
        """Test con número de cartones inválido"""
        output_file = os.path.join(self.test_output_dir, "test_invalid.pdf")

        with self.assertRaises(ValueError):
            generate_pdf(
                output_file=output_file,
                cards_per_page=0
            )

    def test_generate_pdf_mismatched_layout(self):
        """Test con layout que no coincide"""
        output_file = os.path.join(self.test_output_dir, "test_mismatch.pdf")

        with self.assertRaises(ValueError):
            generate_pdf(
                output_file=output_file,
                cards_per_page=6,
                cards_per_row=2,
                cards_per_column=2  # 2×2 = 4 ≠ 6
            )


class TestIntegration(unittest.TestCase):
    """Tests de integración"""

    def test_full_workflow(self):
        """Test del flujo completo de generación"""
        output_dir = "tests/integration_output"
        os.makedirs(output_dir, exist_ok=True)

        try:
            output_file = os.path.join(output_dir, "integration_test.pdf")

            # Generar PDF con todas las opciones
            result = generate_pdf(
                output_file=output_file,
                num_pages=2,
                cards_per_page=6,
                free_text="OH",
                cards_per_row=3,
                cards_per_column=2,
                export_numbers=True
            )

            # Verificaciones
            self.assertTrue(result["success"])
            self.assertEqual(result["total_cards"], 12)
            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(os.path.exists(result["json_file"]))

            # Verificar tamaño del archivo PDF
            self.assertGreater(os.path.getsize(output_file), 1000)

            # Verificar estructura del JSON
            with open(result["json_file"], 'r') as f:
                data = json.load(f)
                self.assertIn("generated_at", data)
                self.assertIn("total_cards", data)
                self.assertIn("cards", data)
                self.assertEqual(len(data["cards"]), 12)

        finally:
            # Limpieza
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    os.remove(os.path.join(output_dir, file))
                os.rmdir(output_dir)


if __name__ == "__main__":
    unittest.main()
