"""Custom forms module."""
import pandas as pd
from django import forms
from .models import MapLayer


class LayerUploadForm(forms.Form):
    """
    Форма для загрузки слоёв карты. Содержит поля для названия слоя, выбора типа слоя и загрузки файла данных.

    Поля:
    - layer_name: Название слоя (CharField) - обязательное поле для указания понятного названия слоя.
    - layer_type: Тип слоя (ChoiseFiled) - выбор одного из предложенных типов слоя (полигоны, маркеры, маршруты, тепловая карта)
    - layer_file: Файл данных (FileField) - загрузка файла в одном из поддерживаемых форматов (CSV).

    Валидирует CSV-файлы в зависимости от типа слоя.
    Для полигонов проверяет обязательные поля: id, name, coordinates.
    """

    layer_name = forms.CharField(
        max_length=255,
        label="Название слоя",
        help_text="Укажите название для вашего слоя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите название слоя"
        })
    )

    layer_type = forms.ChoiceField(
        choices=MapLayer.LAYER_TYPES,
        label="Тип слоя",
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )

    layer_file = forms.FileField(
        label="Файл данных",
        help_text="Загрузите файл в формате CSV",
        widget = forms.FileInput(attrs={
            "class": "form-control",
        })
    )

    def clean_layer_file(self) -> pd.DataFrame:
        """
        Метод для валидации загружаемого CSV-файла.

        Returns:
            pd.DataFrame: Проверенные данные

        Raises:
            ValidationError: Если файл не CSV или нет обязательных полей.
        """
        file = self.cleaned_data['layer_file']

        if not file.name.endswith(".csv"):
            raise forms.ValidationError("Неподдерживаемый формат файла. Поддерживаются: CSV")

        try:
            df = pd.read_csv(file)
        except Exception as e:
            raise forms.ValidationError(f"Ошибка чтения CSV: {e}")

        if self.cleaned_data.get('layer_type') == 'polygons':
            required_columns = {'id', 'name', 'coordinates'}
            if not required_columns.issubset(df.columns):
                raise forms.ValidationError(f"Для полигонов обязательные поля: {', '.join(required_columns)}")
        return f"{file}"















class RouteForm(forms.Form):
    start_latitude = forms.FloatField(
        label='Широта начальной точки',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step':'0.000001', 'placeholder':'Например: 55.812449'})
    )
    start_longitude = forms.FloatField(
        label='Долгота начальной точки',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step':'0.000001', 'placeholder':'Например: 37.454097'})
    )
    end_latitude = forms.FloatField(
        label='Широта конечной точки',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step':'0.000001', 'placeholder':'Например: 55.704070'})
    )
    end_longitude = forms.FloatField(
        label='Долгота конечной точки',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step':'0.000001', 'placeholder':'Например: 37.507868'})
    )
