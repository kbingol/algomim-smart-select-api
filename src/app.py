"""
Module: app.py
Description: This module contains the main Flask application for processing architect algorithm.

Contents:
- index: Flask route for processing product validations and returning a JSON response.

Note: index function has no args. It uses request.json

"""
import os
import logging
import uuid
from functools import partial

from flask import Flask, json, request, jsonify
from flask_cors import CORS
from methods.genetic import Genome, Population, Crossover, Mutation
from methods.colorsimilarity import Color, ColorFeatureExtractor, ColorGrayScaleIdentifier, HueScore, SaturationScore, \
    ValueScore
from database import (
    require_key,
    Products,
    GenomeLimitCalculator,
    ProductListConverter,
    ProductFilter,
    GenomeToProduct, SimilarityChecker
)

app = Flask(__name__)
CORS(app)


def fitness(genome, products):
    colors = []
    c_score = 0
    g_score = 0
    for index, product in enumerate(
            GenomeToProduct(
                genome=genome,
                products=products
            ).get_products_by_genome().values()):
        colors.append(product['color'][0])

    colors = [Color(color).hex() for color in colors]
    gray_colors = [
        gray_color for gray_color in colors if
        ColorGrayScaleIdentifier(color=gray_color).is_gray(threshold=12)
    ]

    colored_colors = [
        colored_color for colored_color in colors if
        not ColorGrayScaleIdentifier(color=colored_color).is_gray(threshold=12)
    ]

    if len(gray_colors) > 1:
        gray_hsv_features = [ColorFeatureExtractor(gray_color).hue() for gray_color in gray_colors]
        g_hue_similarity_score = HueScore(gray_hsv_features).calculate()
        g_saturation_similarity_score = SaturationScore(gray_hsv_features).calculate()
        # c_value_similarity_score = ValueScore(colored_hsv_features).calculate()

        if g_hue_similarity_score > 0.20 and g_saturation_similarity_score > 0.60:
            g_score += g_hue_similarity_score

        else:
            g_score += g_hue_similarity_score / 2

    else:
        g_score += 0.99

        # TODO: Compare saturation and value of the colored and gray colors.

    if len(colored_colors) > 1:
        colored_hsv_features = [ColorFeatureExtractor(colored_color).hue() for colored_color in colored_colors]
        c_hue_similarity_score = HueScore(colored_hsv_features).calculate()
        c_saturation_similarity_score = SaturationScore(colored_hsv_features).calculate()
        # c_value_similarity_score = ValueScore(colored_hsv_features).calculate()

        if c_hue_similarity_score > 0.95 and c_saturation_similarity_score > 0.40:
            c_score += c_hue_similarity_score

        else:
            c_score += c_hue_similarity_score / 2

        # print(hue_similarity_score, saturation_similarity_score, value_similarity_score)

    else:
        c_score += 0.99

    total_scores = g_score + c_score

    # Keep middle
    if total_scores / 2 > 0.45:
        return total_scores / 2
    else:
        return 0.0


def run_evolution(limits, size, generation, fitness):
    population = Genome(limits).make_population(size)

    for i in range(generation):
        population = sorted(
            population,
            key=lambda genome: fitness(genome=genome),
            reverse=True
        )

        if fitness(genome=population[0]) == 0:
            break

        next_generation = population[0:2]

        for spring in range(int(len(population) / 2) - 1):
            parents = Population(population=population).select(fitness_function=fitness)
            offspring_a, offspring_b = Crossover(parents[0], parents[1]).single_point_crossover()
            offspring_a = Mutation(genome=offspring_b, limits=limits).make_linear_mutation()
            offspring_b = Mutation(genome=offspring_b, limits=limits).make_linear_mutation()

            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = SimilarityChecker(population).remove_similar_lists(threshold=3)

    return population


@app.route('/generate', methods=['POST'])
@require_key
def generate():
    """
    Welcoming to the app in index

    Args:
        There is no args.

    Returns:
        flask.Response: A Flask response to say hello
    """

    try:
        # Get brand
        brand = request.headers['brand']

        # Get products by brand then filter by requested types.
        products = Products(brand=brand).get_products_by_brand()
        # Convert product list to single dict to calculate genome limits and filter products.
        products_dict = ProductListConverter(products=products).convert_to_dictionary()
        filtered_products = ProductFilter(
            requested_product_types=request.get_json()["requirements"],
            products=products_dict
        ).find_requested_products_by_types()

        genome_limits = GenomeLimitCalculator(product_dict=filtered_products).calculate_genome_limits()

        fitness_func = partial(
            fitness,
            products=filtered_products,
        )

        evaluated_combinations = run_evolution(limits=genome_limits, size=12, generation=16, fitness=fitness_func)
        print(evaluated_combinations)

        recommendations = []
        for genome in evaluated_combinations:

            if fitness_func(genome=genome, products=filtered_products) > 0.93:
                data = {
                    "id": str(uuid.uuid4()),
                    "products": GenomeToProduct(genome=genome, products=filtered_products).get_products_by_genome(),
                    "score": fitness_func(genome=genome, products=filtered_products),
                    "price": sum(
                        [(float(product['price']) * float(request.get_json()["requirements"][index]["value"])) for
                         index, product in enumerate(
                            (GenomeToProduct(genome=genome,
                                             products=filtered_products).get_products_by_genome().values()))])

                }

                recommendations.append(data)

        # print(recommendations)

        # Return Results

        return jsonify(recommendations), 200

    except Exception as e:
        # Log the exception
        logging.exception("An error occurred while processing the request: %s", str(e))

        # Continue the execution and return a response indicating a temporary issue
        error_response = {
            "error": "An unexpected error occurred. Please try again later."
        }

        return app.response_class(
            response=json.dumps(error_response),
            status=200,
            mimetype='application/json'
        )


@app.route('/', methods=['GET'])
def index():
    """
    Welcoming to the app in index

    Args:
        There is no args.

    Returns:
        flask.Response: A Flask response to say hello
    """

    try:
        return app.response_class(
            response=json.dumps({"message": "First API"}),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Log the exception
        logging.exception("An error occurred while processing the request: %s", str(e))

        # Continue the execution and return a response indicating a temporary issue
        error_response = {
            "error": "An unexpected error occurred. Please try again later."
        }

        return app.response_class(
            response=json.dumps(error_response),
            status=200,
            mimetype='application/json'
        )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
