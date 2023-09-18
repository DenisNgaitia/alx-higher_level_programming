#!/usr/bin/python3

import json
import csv
import turtle

"""Base class serving as a foundation for other classes"""
class Base:
    """Class variable to keep track of instance count"""
    __nb_objects = 0

    def __init__(self, id=None):
        """Initialize an instance with an optional provided 'id'"""
        if id is not None:
            self.id = id
        else:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects

    """Convert a list of dictionaries to a JSON string"""
    @staticmethod
    def to_json_string(list_dictionaries):
        if list_dictionaries is None:
            return "[]"
        return json.dumps(list_dictionaries)

    """Write the JSON representation of objects to a file"""
    @classmethod
    def save_to_file(cls, list_objs):
        filename = cls.__name__ + ".json"
        with open(filename, "w") as f:
            if list_objs is None:
                f.write("[]")
            else:
                list_dicts = [obj.to_dictionary() for obj in list_objs]
                f.write(Base.to_json_string(list_dicts))

    """Convert a JSON string to a list of dictionaries"""
    @staticmethod
    def from_json_string(json_string):
        if not json_string:
            return []
        return json.loads(json_string)

    """Create an instance with attributes from a dictionary"""
    @classmethod
    def create(cls, **dictionary):
        polygons = {
            'Rectangle': (1, 1, 0, 0),
            'Square': (1, 0, 0, None)
        }
        if cls.__name__ in polygons:
            polygon = cls(*polygons[cls.__name__])
            polygon.update(**dictionary)
            return polygon

    """Load a list of instances from a JSON file"""
    @classmethod
    def load_from_file(cls):
        filename = cls.__name__ + ".json"
        try:
            with open(filename, encoding="utf-8") as f:
                list_instances = cls.from_json_string(f.read())
                return [cls.create(**d) for d in list_instances]
        except IOError:
            return []

    """Build fieldnames for CSV reader or writer based on the class"""
    @staticmethod
    def _build_fieldnames(c):
        if c.__name__ == "Rectangle":
            return ["id", "width", "height", "x", "y"]
        else:
            return ["id", "size", "x", "y"]

    """Serialize a list of objects into CSV format and save to a file"""
    @classmethod
    def save_to_file_csv(cls, list_objs):
        filename = cls.__name__ + ".csv"
        with open(filename, "w", encoding="utf-8") as f:
            if list_objs is None or list_objs == []:
                f.write("[]")
            else:
                writer = csv.DictWriter(f, fieldnames=cls._build_fieldnames(cls))
                for obj in list_objs:
                    writer.writerow(obj.to_dictionary())

    """Deserialize a CSV string representation into a list of instances"""
    @classmethod
    def load_from_file_csv(cls):
        filename = cls.__name__ + ".csv"
        try:
            with open(filename, encoding="utf-8") as f:
                reader = csv.DictReader(f, fieldnames=cls._build_fieldnames(cls))
                list_dicts = [dict((k, int(v)) for k, v in d.items()) for d in reader]
                return [cls.create(**d) for d in list_dicts]
        except IOError:
            return []

    """Draw rectangles and squares using Turtle graphics"""
    @staticmethod
    def draw(list_rectangles, list_squares):
        t = turtle.Turtle()
        t.screen.bgcolor("brown")
        t.hideturtle()

        def show(color, objects):
            t.color(color)
            for obj in objects:
                t.penup()
                t.goto(obj.x, obj.y)
                t.pendown()

                for i in range(2):
                    t.forward(obj.width)
                    t.left(90)
                    t.forward(obj.height)
                    t.left(90)

        show("gold", list_rectangles)
        show("magenta", list_squares)

        turtle.exitonclick()
