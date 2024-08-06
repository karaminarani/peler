import base64
from typing import Optional


class URLSafe:
    @staticmethod
    def add_padding(data_string: str) -> str:
        """
        Adds padding to the data string to make its length a multiple of 4.

        Args:
            data_string (str): The data string to which padding will be added.

        Returns:
            str: The padded data string.
        """
        return data_string + "=" * (-len(data_string) % 4)

    @staticmethod
    def del_padding(data_string: str) -> str:
        """
        Removes padding from the data string.

        Args:
            data_string (str): The data string from which padding will be removed.

        Returns:
            str: The data string without padding.
        """
        return data_string.rstrip("=")

    def encode_data(self, data_integer: int) -> str:
        """
        Encodes an integer into a URL-safe base64 string.

        Args:
            data_integer (int): The integer to encode.

        Returns:
            str: The URL-safe base64 encoded string.
        """
        data_bytes = str(data_integer).encode("utf-8")
        encoded_data = base64.urlsafe_b64encode(data_bytes)
        return self.del_padding(encoded_data.decode("utf-8"))

    def decode_data(self, data_string: str) -> Optional[str]:
        """
        Decodes a URL-safe base64 string back into the original integer string.

        Args:
            data_string (str): The URL-safe base64 string to decode.

        Returns:
            Optional[str]: The decoded integer string, or None if decoding fails.
        """
        try:
            data_padding = self.add_padding(data_string)
            encoded_data = base64.urlsafe_b64decode(data_padding)
            return encoded_data.decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            return None


url_safe: URLSafe = URLSafe()
