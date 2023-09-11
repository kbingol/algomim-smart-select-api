import json
from functools import wraps
import firebase_admin
from firebase_admin import firestore
from flask import request

default_app = firebase_admin.initialize_app()


class Products:
    def __init__(self, brand):
        self.brand = brand

    def get_products_by_brand(self):
        return firestore.client().collection("products").document(self.brand).get().to_dict()['products']


class GenomeToProduct:
    def __init__(self, products, genome):
        self.genome = genome
        self.products = products

    def get_products_by_genome(self):
        result = {}
        for index, (key, values) in enumerate(self.products.items()):
            if 0 <= self.genome[index] < len(values):
                result[key] = values[self.genome[index]]
        return result


class ProductFilter:
    def __init__(self, requested_product_types, products):
        self.requested_product_types = requested_product_types
        self.products = products

    def find_requested_products_by_types(self):
        requested_type_ids = set(item['id'] for item in self.requested_product_types)
        return {key: self.products[key] for key in self.products if key in requested_type_ids}


class ProductListConverter:
    def __init__(self, products):
        self.products = products

    def convert_to_dictionary(self):
        result_dict = {}
        for dictionary in self.products:
            for key, value in dictionary.items():
                result_dict[key] = value
        return result_dict


class GenomeLimitCalculator:
    def __init__(self, product_dict):
        self.product_dict = product_dict

    def calculate_genome_limits(self):
        return [len(value) - 1 for value in self.product_dict.values()]


class KeyValidator:
    def __init__(self):
        self.db = firestore.client()

    def validate_key(self, key):
        key_reference = self.db.collection("users").where("key", "==", key)
        count_reference = key_reference.count()
        results = count_reference.get()
        return results[0][0].value > 0


key_validator = KeyValidator()


class SimilarityChecker:
    def __init__(self, objects):
        self.objects = objects

    @staticmethod
    def calculate_similarity(list1, list2):
        return sum(1 for x, y in zip(list1, list2) if x == y)

    def remove_similar_lists(self, threshold):
        unique_population = [self.objects[0]]  # Initialize with the first list

        for new_list in self.objects[1:]:
            is_similar = False
            for existing_list in unique_population:
                similarity = self.calculate_similarity(new_list, existing_list)
                if similarity >= threshold:
                    is_similar = True
                    break
            if not is_similar:
                unique_population.append(new_list)

        return unique_population


class CombinationPriceCalculator:
    def __init__(self, products, requirements):
        self.products = products
        self.requirements = requirements

    def calculate(self):
        print(p)
        return 0

def require_key(view_func):
    """
    Decorator to require a valid API key (secret key) for accessing a view function.

    Args:
        view_func (function): The view function that requires authentication.

    Returns:
        function: The decorated function that handles API key validation.

    Note:
        The `validate_key` method of the `KeyValidator` class is used to validate the API key.
        It queries a Firebase database to check the token's validity. If valid, the view function
        is executed; otherwise, it returns a JSON response with an "Invalid API key"
        error and a 401 status code (Unauthorized).
    """

    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        secret_key = request.headers.get("secret-key")
        if secret_key and key_validator.validate_key(secret_key):
            return view_func(*args, **kwargs)
        else:
            return json.dumps({"error": "Invalid API key"}), 401

    return decorated_function


if __name__ == "__main__":
    print("")
