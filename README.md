## Django Model Seeder

[![GitHub stars](https://img.shields.io/github/stars/christiangarcia0311/django-model-seeder?style=social)](https://github.com/christiangarcia0311/django-model-seeder/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/christiangarcia0311/django-model-seeder?style=flat)](https://github.com/christiangarcia0311/django-model-seeder/issues)
![Static Badge](https://img.shields.io/badge/License-MIT-orange?style=flat)
![Static Badge](https://img.shields.io/badge/Github-django_model_seeder-green?style=flat&logo=github)
![Static Badge](https://img.shields.io/badge/Pypi-django_model_seeder-blue?style=flat&logo=pypi&logoColor=white)
![Static Badge](https://img.shields.io/badge/Django-5.2+-green?style=flat&logo=django&logoColor=white)
![Static Badge](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python&logoColor=white)
[![Last commit](https://img.shields.io/github/last-commit/christiangarcia0311/django-model-seeder?style=flat)](https://github.com/christiangarcia0311/django-model-seeder/commits/main)
[![Latest release](https://img.shields.io/github/v/release/christiangarcia0311/django-model-seeder?style=flat)](https://github.com/christiangarcia0311/django-model-seeder/releases/latest)

**Command-based synthetic data generation and seeding for Django models using [data-seed-ph](https://github.com/christiangarcia0311/data-seed-ph).**

>[!NOTE]
> Designed for rapid database population in development environments, API testing, QA automation, and demo applications with seamless integration to Django's management command system.

#### Why Django Model Seeder

Populating Django databases with realistic test data can be repetitive and time-consuming. Django Model Seeder simplifies this process by offering powerful management commands that automatically generate realistic Philippine-based synthetic data and insert it directly into your Django models, eliminating the need for manual data seeding scripts.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
  - [JSON Configuration](#json-configuration)
  - [YAML Configuration](#yaml-configuration)
- [Management Commands](#management-commands)
  - [seed_models](#1-seed_models-command)
  - [clear_seeds](#2-clear_seeds-command)
  - [list_seeds](#3-list_seeds-command)
- [Data Generation Types](#data-generation-types)
- [Advanced Usage](#advanced-usage)
- [Use Cases](#use-cases)
- [Important Notes](#important-notes)
- [Troubleshooting](#troubleshooting)
- [Library Source](#library-source)
- [License](#license)

### Installation

Install via python package index [Pypi]().

```bash
pip install django-model-seeder
```

### Quick Start

Add `django_seeder` to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_seeder',
    'your_app_name',
]
```

Create Database model in your `app/models.py` file:

```python
from django.db import models

class Artist(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
```

Create `fixtures/seed_config.json` file:

```json
{
    "Artist": {
        "app_label": "music_app",
        "rows": 30,
        "mapping": {
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email"
        }
    }
}
```

Run seeding command:

```bash
python manage.py seed_models --config fixtures/seed_config.json
```

Output of the command and check your database for confirmation:

```bash
Loaded config from fixtures/seed_config.json
Seeding successfully completed
Artist: 30 rows seeded
```

## Configuration

### JSON Configuration

Define your seeding configuration in JSON format:

```json
{
    "ModelName": {
        "app_label": "app_label_name",
        "rows": "number_of_rows",
        "mapping": {
            "field_name": "data_generator_keyword_or_custom_values"
        }
    }
}
```

#### Example:

```json
{
    "Artist": {
        "app_label": "music_app",
        "rows": 30,
        "mapping": {
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email",
            "birthdate": "birthdate"
        }
    },
    "Album": {
      "app_label": "music_app",
        "rows": 100,
        "mapping": {
            "category": ["Jazz", "Rock", "RnB"],
            "rating": [0.0, 5.0, "float"],
            "views": [0, 50000]
        }
    }
}
```

### YAML Configuration

Define your seeding configuration in YAML format:

```yaml
Artist:
    app_label: app_label_name
    rows: number_of_rows
    mapping:
        field_name: data_generator_keyword_or_custom_values
```

#### Example:

```yaml
Artist:
    app_label: music_app
    rows: 50
    mapping:
        firstname: firstname
        lastname: lastname
        email: email
        birthdate: birthdate
Album:
    rows: 100
    mapping: 
        category:
            - Jazz
            - Rock
            - RnB
        rating:
            - 0.0
            - 5.0
            - float
        views:
            - 0
            - 50000
```

## Management Commands

#### **1. `seed_models` command**

Seed Django models with synthetic data from configuration files or direct arguments.

**Syntax**:

```bash
python manage.py seed_models [OPTIONS]
```

**Options**:

| Option | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `--config` | str | None | Path to seed configuration file (JSON or YAML) |
| `--model` | str | None | Specific model to seed (format: ModelName) |
| `--app` | str | None | Django app label |
| `--rows` | int | 10 | Number of rows to seed |
| `--clear` | flag | False | Clear existing data before seeding |
| `--dry-run` | flag | False | Show what would be seeded without actually seeding |
| `--verbose` | flag | False | Show detailed output including sample records |

**Examples**

From configuration file:

```bash
python manage.py seed_models --config fixtures/seed_config.json
```

From configuration file with verbose output:

```bash
python manage.py seed_models --config fixtures/seed_config.json --verbose
```

Clear existing data and reseed:

```bash
python manage.py seed_models --config fixtures/seed_config.json --clear
```

Dry run preview:

```bash
python manage.py seed_models --config fixtures/seed_config.json --dry-run
```

Seed specific model or auto-generated mapping with arguments:

```bash
python manage.py seed_models --model Artist --app music_app --rows 50
```

Seed specific model and clear first:

```bash
python manage.py seed_models --model Artist --app music_app --rows 50 
```

#### **2. `clear_seeds` command**

Clear seeded data from Django models.

**Syntax**:

```bash
python manage.py clear_seeds [OPTIONS]
```

**Options**:

| Option | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `--model` | str | None | Specific model to clear (format: ModelName) |
| `--app` | str | None | Django app label |
| `--all` | flag | False | Clear data from all models |
| `--confirm` | flag | False | Skip confirmation prompt |


**Examples**

Clear specific model with confirmation:

```bash
python manage.py clear_seeds --model Artist --app music_app
```

Clear specific model without confirmation:

```bash
python manage.py clear_seeds --model Artist --app music_app --confirm
```

Clear all seeded data with confirmation:

```bash
python manage.py clear_seeds --all
```

Clear all seeded data without confirmation:

```bash
python manage.py clear_seeds --all --confirm
```

#### **3. `list_seeds` command**

List all available Django models for seeding with optional record counts.

**Syntax**:

```bash
python manage.py list_seeds [OPTIONS]
```

**Options**:

| Option | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `--app` | str | None | Django app label |
| `--count` | flag | False | Show record count each model |

**Examples**

List all available models:

```bash
python manage.py list_seeds
```

List models in specific app:

```bash
python manage.py list_seeds --app music_app
```

List models with record counts:

```bash
python manage.py list_seeds --count
```

List models in specific app with counts:

```bash
python manage.py list_seeds --app music_app --count
```

## Data Generation Types

**1. String Keywords**

Use built-in data generators with string keywords from [Data Seed PH](https://github.com/christiangarcia0311/data-seed-ph?tab=readme-ov-file#features).

**Examples**

```json
{
    "Artist": {
        "app_label": "music_app",
        "rows": 30,
        "mapping": {
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email",
            "birthdate": "birthdate"
        }
    }
}
```

**2. Numeric Ranges (Tuples)**

Generate random integers ot floats within specified ranges.

> [!NOTE]
> JSON lists are converted into tuples when generating data with specified ranges.

```json
{
    "Album": {
        "app_label": "music_app",
        "rows": 100,
        "mapping": {
            "likes": [0, 100000],
            "rating": [0.0, 5.0, "float"],
            "views": [0, 50000]
        }
    }
}
```

**Format**

- Integer range: `[min, max]`
- Float range: `[min, max, "float"]`


**3. Categorical Values (Lists)**

Choose randomly from predefined options.

```json
{
    "Album": {
        "app_label": "music_app",
        "rows": 100,
        "mapping": {
            "catgeory": ["RnB", "Rock", "Hip-Hop", "Jazz"],
            "album_type": ["Studio Album", "Live Album", "Single", "EP"],
            "release_format": ["Digital", "CD"]
        }
    }
}
```

**4. Parameterized Keywords**

Some generators accept parameters using colon syntax:

> [!NOTE]
> Parameterized keywords only available in `AddressDataProvider` provider within [Data Seed PH](https://github.com/christiangarcia0311/data-seed-ph?tab=readme-ov-file#features) library.

```json
{
  "Location": {
    "app_label": "geoprroject",
    "rows": 30,
    "mapping": {
      "addr_province": "province:Surigao Del Norte",
      "addr_municipality": "municipality:Claver",
      "addr_barangay": "barangay"
    }
  }
}
```

**Supported field types**

- `CharField`, `TextField`: string keywords or lists
- `IntegerField`: tuples with int range
- `FloatField`: tuples with float range
- `DateField`: date keywords like `birthdate`
- `EmailField`: `email` keyword
- `ForeignKey`: handled programmatically (see [Advanced Usage](#advanced-usage))

### Advanced Usage

**Models with Foreign Key Relations**

Seed models with foreign key relationships using the `relations` key in your configuration file.

Example Django Models in `music_app/models.py`:

```python
from django.db import models

class Artist(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    age = models.IntegerField()

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    description = models.TextField()
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    streams = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    feedback = models.TextField()
    email = models.EmailField()
    rating = models.IntegerField()
```

Configuration with Relations (JSON) file in `fixtures/seed_config.json`:

```json
{
  "Artist": {
    "app_label": "music_app",
    "rows": 20,
    "mapping": {
      "firstname": "firstname",
      "lastname": "lastname",
      "email": "email",
      "phone": "mobile",
      "age": [25, 65]
    }
  },
  "Album": {
    "app_label": "music_app",
    "rows": 100,
    "mapping": {
      "title": ["Echoes of Time", "Midnight Dreams", "Silver Linings"],
      "description": "fulladdress",
      "genre": "course",
      "release_year": [2015, 2024],
      "streams": [0, 1000000],
      "rating": [1.0, 5.0, "float"]
    },
    "relations": {
      "artist": "Artist"
    }
  },
  "Review": {
    "app_label": "music_app",
    "rows": 250,
    "mapping": {
      "reviewer_name": "fullname",
      "feedback": "fulladdress",
      "email": "email",
      "rating": [1, 5]
    },
    "relations": {
      "album": "Album"
    }
  }
}
```

Configuration with Relation (YAML) file in `fixtures/seed_config.yaml`:

```yaml
Artist:
  app_label: music_app
  rows: 20
  mapping:
    firstname: firstname
    lastname: lastname
    email: email
    phone: mobile
    age:
      - 25
      - 65

Album:
  app_label: music_app
  rows: 100
  mapping:
    title:
      - Echoes of Time
      - Midnight Dreams
      - Silver Linings
    description: fulladdress
    genre: course
    release_year:
      - 2015
      - 2024
    streams:
      - 0
      - 1000000
    rating:
      - 1.0
      - 5.0
      - float
  relations:
    artist: Artist

Review:
  app_label: music_app
  rows: 250
  mapping:
    reviewer_name: fullname
    feedback: fulladdress
    email: email
    rating:
      - 1
      - 5
  relations:
    album: Album
```

**How Relations Work**

The `relations` key links foreign keys to parent models:

- `"artist": "Artist"`: Each Album gets a random Artist from existing Artist records
- `"album": "Album"`: Each Review gets a random Album from existing Album records

### Use Cases

- **Development**: Populate databases with realistic test data during development

- **Testing**: Seed test databases for integration and end-to-end tests

- **API Testing**: Generate test payloads and bulk request data for API endpoint testing

- **QA Automation**: Quickly set up test databases for QA testing cycles

- **Demo Applications**: Build convincing demos with realistic Philippine synthetic data

- **Load Testing**: Create large datasets for performance and stress testing

- **Staging Environments**: Pre-populate staging databases with realistic data

- **Documentation**: Generate example data for README and API documentation

- **Database Backup Testing**: Restore and verify database backups with synthetic data

### Important Notes

> [!IMPORTANT]
> Synthetic Data Disclaimer: All generated data is random and synthetic. It does NOT represent real individuals, real addresses, or real contact information. Use this library only for development, testing, and non-production environments.

> [!TIP]
> Related Library: Django Model Seeder uses [data-seed-ph](https://github.com/christiangarcia0311/data-seed-ph) library for authentic Philippine synthetic data generation.

> [!WARNING]
> Avoid seeding production databases. Always use this library in development and testing environments only.

### Troubleshooting

**1. Command Not Found**

**Error:** `django.core.management.base.CommandError: No app with label 'django_seeder'`

**Solution:** Ensure `django_seeder` is added to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'django_seeder',
    ...
]
```

**2. Configuration File Not Found**

**Error:** `FileNotFoundError: Configuration file not found`

**Solution:** Ensure the config file path is correct and relative to your project root

```bash
python manage.py seed_models --config fixtures/seed_config.json
```

**3. Import Errors**

**Error:** `ModuleNotFoundError: No module named 'data_seed_ph'`

**Solution:** Install the dependency

```bash
pip install data-seed-ph
```

**4. Module Not Found**

**Error:** `LookupError: Model not found: myapp.Author`

**Solution:** Verify app label and model name are correct

```bash
python manage.py list_seeds
```

**5. Invalid JSON Configuration**

**Error:** `InvalidConfigurationError: Invalid configuration file format`

**Solution:** Validate JSON syntax using an online validate or:

```bash
python -m json.tool fixtures/seed_config.json
```

### Library Source 

- [Data Seed PH](https://github.com/christiangarcia0311/data-seed-ph)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Management Commands](https://docs.djangoproject.com/en/6.0/howto/custom-management-commands/)

### Releases

[See releases](https://github.com/christiangarcia0311/django-model-seeder/releases)

### License

MIT License - See [LICENSE](/LICENSE) file for details.


### Author

[<img src="https://github.com/christiangarcia0311.png" width="80px;" style="border-radius: 100%;">](https://github.com/christiangarcia0311)

