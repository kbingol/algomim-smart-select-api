from colorsys import rgb_to_hsv

from colorsys import rgb_to_hsv
from itertools import combinations


class Color:
    """
    Represents a color.
    """

    def __init__(self, color):
        """
        Initialize the Color object with a color value.

        :param color: The color value.
        """
        self.color = color

    def hex(self):
        """
        Get the hexadecimal representation of the color.

        :return: Hexadecimal color representation.
        """
        return self.color.lstrip("#") if self.color.startswith("#") else self.color


class HexValidator:
    """
    Validates hexadecimal color codes.
    """

    def __init__(self, color):
        """
        Initialize the HexValidator object with a color value.

        :param color: The color value.
        """
        self.color = color

    def is_valid(self):
        """
        Check if the color is a valid hexadecimal color code.

        :return: True if valid, False otherwise.
        """
        return all(c in "0123456789ABCDEFabcdef" for c in self.color) and len(self.color) == 6


class ColorGrayScaleIdentifier:
    """
    Identifies if a color is grayscale.
    """

    def __init__(self, color):
        """
        Initialize the ColorGrayScaleIdentifier object with a color value.

        :param color: The color value.
        """
        self.color = color

    def is_gray(self, threshold):
        """
        Check if the color is grayscale within a specified threshold.

        :param threshold: The threshold for identifying grayscale.
        :return: True if grayscale, False otherwise.
        """
        r, g, b = int(self.color[0:2], 16), int(self.color[2:4], 16), int(self.color[4:6], 16)
        return abs(r - g) <= threshold and abs(r - b) <= threshold and abs(g - b) <= threshold


class ColorFeatureExtractor:
    """
    Extracts features from a color.
    """

    def __init__(self, color):
        """
        Initialize the ColorFeatureExtractor object with a color value.

        :param color: The color value.
        """
        self.color = color

    def rgb_to_hsv(self):
        """
        Convert the color from RGB to HSV color space.

        :return: HSV color representation.
        """
        rgb_color = int(self.color[0:2], 16), int(self.color[2:4], 16), int(self.color[4:6], 16)
        hsv_color = rgb_to_hsv(rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0)
        return hsv_color

    def hue(self):
        """
        Get the hue value of the color.

        :return: Hue value.
        """
        hsv_color = self.rgb_to_hsv()
        return hsv_color[0]

    def saturation(self):
        """
        Get the saturation value of the color.

        :return: Saturation value.
        """
        hsv_color = self.rgb_to_hsv()
        return hsv_color[1]

    def value(self):
        """
        Get the value (brightness) of the color.

        :return: Value (brightness) of the color.
        """
        hsv_color = self.rgb_to_hsv()
        return hsv_color[2]


class Similarity:
    """
    Represents similarity between two values.
    """

    def __init__(self, value_1: float, value_2: float):
        """
        Initialize the Similarity object with two values.

        :param value_1: The first value.
        :param value_2: The second value.
        """
        self.value_1 = value_1
        self.value_2 = value_2

    def calculate(self):
        """
        Calculate the similarity between the two values.

        :return: Similarity value.
        """
        raise NotImplementedError("Subclasses must implement the calculate method")


class HueSimilarity(Similarity):
    """
    Calculates similarity based on hue values.
    """

    def calculate(self):
        """
        Calculate the similarity based on hue values.

        :return: Hue similarity value.
        """
        hue_difference = min(abs(self.value_1 - self.value_2), 1 - abs(self.value_1 - self.value_2))
        return float(1 - hue_difference)


class SaturationSimilarity(Similarity):
    """
    Calculates similarity based on saturation values.
    """

    def calculate(self):
        """
        Calculate the similarity based on saturation values.

        :return: Saturation similarity value.
        """
        saturation_difference = abs(self.value_1 - self.value_2)
        return float(1 - saturation_difference)


class ValueSimilarity(Similarity):
    """
    Calculates similarity based on value (brightness) values.
    """

    def calculate(self):
        """
        Calculate the similarity based on value values.

        :return: Value similarity value.
        """
        value_difference = abs(self.value_1 - self.value_2)
        return float(1 - value_difference)


class HueScore:
    def __init__(self, hue_features):
        self.hue_features = hue_features

    def calculate(self):
        hue_scores = [
            1 - (min(abs(value_1 - value_2), 1 - abs(value_1 - value_2)))
            for (index_a, value_1), (index_b, value_2)
            in combinations(enumerate(self.hue_features), 2)
        ]

        avg_hue_score = sum(hue_scores) / len(hue_scores)

        return avg_hue_score


class SaturationScore:
    def __init__(self, saturation_features):
        self.saturation_features = saturation_features

    def calculate(self):
        saturation_scores = [
            (1 - abs(value_1 - value_2))
            for (index_a, value_1), (index_b, value_2) in
            combinations(enumerate(self.saturation_features), 2)
        ]

        avg_saturation_score = sum(saturation_scores) / len(saturation_scores)

        return avg_saturation_score


class ValueScore:
    def __init__(self, value_features):
        self.value_features = value_features

    def calculate(self):
        value_scores = [
            (1 - abs(value_1 - value_2))
            for (index_a, value_1), (index_b, value_2) in
            combinations(enumerate(self.value_features), 2)
        ]

        avg_value_score = sum(value_scores) / len(value_scores)

        return avg_value_score






if __name__ == "__main__":
    colors = ["#D9D9D9", "AAAAAA", "#7E7E7E", "86A5B9", "#8DB8D4"]
    standard_colors = [Color(color).hex() for color in colors]
    features = [ColorFeatureExtractor(color) for color in standard_colors]
    hue_f = [color_feature.saturation() for color_feature in features]

    """
    standard_color = Color(colors[4]).hex()
    print(standard_color)

    is_gray = ColorGrayScaleIdentifier(standard_color).is_gray(threshold=12)
    print(is_gray)


 
        
 
    extractor = ColorFeatureExtractor("8DB8D4")
    hue_value = extractor.hue()
    saturation_value = extractor.saturation()
    value_value = extractor.value()

    print("Hue:", hue_value)
    print("Saturation:", saturation_value)
    print("Value:", value_value)

    hue_similarity = HueSimilarity(0.99450, 0.86964).calculate()
    print(hue_similarity)
    """
