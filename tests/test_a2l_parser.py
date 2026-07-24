import unittest

from data_manager.a2l_parser import (
    extract_measurement_blocks,
    parse_supported_signals,
)


class A2lParserTests(unittest.TestCase):
    def test_extracts_measurement_and_characteristic_blocks(self):
        text = (
            '/begin MEASUREMENT PbcIn_Speed\n'
            'ECU_ADDRESS 0x100\n'
            '/end MEASUREMENT\n'
            '/begin CHARACTERISTIC PbcOut_Torque\n'
            'VALUE 0x200\n'
            '/end CHARACTERISTIC'
        )

        blocks = extract_measurement_blocks(text)

        self.assertEqual(len(blocks), 2)
        self.assertIn('PbcIn_Speed', blocks[0])
        self.assertIn('PbcOut_Torque', blocks[1])

    def test_parses_only_supported_signals_and_addresses(self):
        text = (
            '/begin MEASUREMENT PbcIn_Speed\n'
            'ECU_ADDRESS 0x100\n'
            '/end MEASUREMENT\n'
            '/begin MEASUREMENT UnrelatedSignal\n'
            'ECU_ADDRESS 0x999\n'
            '/end MEASUREMENT\n'
            '/begin CHARACTERISTIC SsmpbOut_State\n'
            'VALUE 0x200\n'
            '/end CHARACTERISTIC'
        )

        self.assertEqual(
            parse_supported_signals(text),
            [
                ('PbcIn_Speed', '0x100'),
                ('SsmpbOut_State', '0x200'),
            ],
        )

    def test_uses_unknown_when_address_is_missing(self):
        text = (
            '/begin MEASUREMENT PbcOut_Status\n'
            '/end MEASUREMENT'
        )

        self.assertEqual(
            parse_supported_signals(text),
            [('PbcOut_Status', 'Unknown')],
        )


if __name__ == '__main__':
    unittest.main()
