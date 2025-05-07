"""Django models module."""
import random
import os
import pandas as pd
from django.db import models
from django.conf import settings
from typing import Dict, Any


class MapLayer(models.Model):
    """
    Модель для представления картографического слоя.

    Атрибуты:
    - name: Название слоя (CharField). Максимальная длина - 255 символов.
    - layer_type: Тип слоя (CharField). Может принимать одно из значений: polygon, marker, route, heatmap. Максимальная длина - 20 символов.
    - csv_file: Файл данных (FileField). Формат CSV, хранится в определенной директории.
    - is_active: Флаг (BooleanField). Отображение слоя на карте.
    - created_at: Дата создания слоя (DateTimeField). Автоматически заполняется временем создания.
    - updated_at: Дата последнего обновления слоя (DateTimeField). Обновляется каждый раз при сохранении модели.

    Методы:
    - __str__: Возвращает строковое представление модели в виде `[название] ([тип слоя])`.
    """

    LAYER_TYPES = (
        ("markers", "Маркер"),
        ("polygons", "Полигон"),
        ("route", "Маршрут"),
        ("heatmap", "Тепловая карта"),
    )

    name = models.CharField("Название слоя", max_length=255)
    layer_type = models.CharField("Тип слоя", max_length=20, choices=LAYER_TYPES)
    csv_file = models.FileField("CSV файл", upload_to="map_layers/")
    is_active = models.BooleanField("Отображать", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_layer_type_display()})"

    @staticmethod
    def get_random_color() -> str:
        """Генерирует случайный HEX-цвет для слоя"""
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def get_processed_data(self) -> Dict[str, Any]:
        """
        Возвращает данные слоя в формате пригодном для Leaflet


        Returns:
            Dict: Данные в GeoJson-подобном формате.
        """
        if self.layer_type == "polygons":
            return self.process_polygon_data()
        return {}

    def process_polygon_data(self) -> Dict[str, Any]:
        """Обрабатывает данные полигонов из CSV."""
        print(f"/{self.csv_file}")
        print(settings.MEDIA_ROOT)
        file_path = os.path.join(settings.MEDIA_ROOT, 'map_layers', f"{self.csv_file}")

        df = pd.read_csv(file_path)
        features = []

        for _, row in df.iterrows():
            features.append({
                "type": "Feature",
                "properties": {
                    "name": row["name"],
                    "color": row.get("color", self.get_random_color()),
                    "text": row.get("text", "")
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [float(x) for x in point.split(",")]
                        for point in row["coordinates"].split(";")
                    ]]
                }
            })
        return {"type": "FeatureCollection", "features": features}

