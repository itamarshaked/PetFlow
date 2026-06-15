from flask import Blueprint, jsonify

docs_bp = Blueprint("docs", __name__)


@docs_bp.get("/openapi.json")
def openapi():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "PetFlow API",
            "version": "1.0.0",
            "description": "PetFlow REST API for user authentication, pet management, and pet image uploads."
        },
        "servers": [
            {"url": "https://petflow.shaked.in"}
        ],
        "tags": [
            {"name": "Health", "description": "Application health checks"},
            {"name": "Authentication", "description": "User registration and login"},
            {"name": "Pets", "description": "Pet CRUD and image upload"}
        ],
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            },
            "schemas": {
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "example": "invalid credentials"}
                    }
                },
                "RegisterRequest": {
                    "type": "object",
                    "required": ["email", "password"],
                    "properties": {
                        "email": {"type": "string", "format": "email", "example": "itamar@example.com"},
                        "password": {"type": "string", "format": "password", "example": "PetFlow123!"}
                    }
                },
                "RegisterResponse": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "user created"},
                        "user_id": {"type": "integer", "example": 1}
                    }
                },
                "LoginRequest": {
                    "type": "object",
                    "required": ["email", "password"],
                    "properties": {
                        "email": {"type": "string", "format": "email", "example": "itamar@example.com"},
                        "password": {"type": "string", "format": "password", "example": "PetFlow123!"}
                    }
                },
                "LoginResponse": {
                    "type": "object",
                    "properties": {
                        "access_token": {
                            "type": "string",
                            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        }
                    }
                },
                "PetRequest": {
                    "type": "object",
                    "required": ["name", "species", "age"],
                    "properties": {
                        "name": {"type": "string", "example": "Dubi"},
                        "species": {"type": "string", "example": "Dog"},
                        "age": {"type": "integer", "example": 4}
                    }
                },
                "PetResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "name": {"type": "string", "example": "Dubi"},
                        "species": {"type": "string", "example": "Dog"},
                        "age": {"type": "integer", "example": 4},
                        "image_url": {
                            "type": "string",
                            "nullable": True,
                            "example": "https://petflow-pet-images-160885257498.s3.eu-central-1.amazonaws.com/dubi.jpg"
                        }
                    }
                },
                "ImageUploadResponse": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "image uploaded"},
                        "image_url": {
                            "type": "string",
                            "example": "https://petflow-pet-images-160885257498.s3.eu-central-1.amazonaws.com/dubi.jpg"
                        }
                    }
                }
            }
        },
        "paths": {
            "/health": {
                "get": {
                    "tags": ["Health"],
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "Application is healthy",
                            "content": {
                                "application/json": {
                                    "example": {"status": "ok"}
                                }
                            }
                        }
                    }
                }
            },
            "/register": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Register a new user",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RegisterRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "User created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/RegisterResponse"}
                                }
                            }
                        },
                        "400": {
                            "description": "Missing email or password",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        },
                        "409": {
                            "description": "User already exists",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/login": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Login and receive a JWT access token",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/LoginResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid credentials",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/pets": {
                "get": {
                    "tags": ["Pets"],
                    "summary": "List all pets",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "List of pets",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/PetResponse"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Pets"],
                    "summary": "Create a new pet",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/PetRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Pet created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/PetResponse"}
                                }
                            }
                        },
                        "401": {"description": "Missing or invalid JWT token"}
                    }
                }
            },
            "/pets/{pet_id}": {
                "parameters": [
                    {
                        "name": "pet_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                        "type": "string",
                        "format": "uuid"
                        },
                        "example": "0798602d-4e13-4e6a-9d89-1651ba2f59a6"
                    }
                ],
                "get": {
                    "tags": ["Pets"],
                    "summary": "Get a pet by ID",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Pet found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/PetResponse"}
                                }
                            }
                        },
                        "404": {"description": "Pet not found"}
                    }
                },
                "put": {
                    "tags": ["Pets"],
                    "summary": "Update a pet",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/PetRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Pet updated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/PetResponse"}
                                }
                            }
                        },
                        "404": {"description": "Pet not found"}
                    }
                },
                "delete": {
                    "tags": ["Pets"],
                    "summary": "Delete a pet",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Pet deleted",
                            "content": {
                                "application/json": {
                                    "example": {"message": "pet deleted"}
                                }
                            }
                        },
                        "404": {"description": "Pet not found"}
                    }
                }
            },
            "/pets/{pet_id}/image": {
                "post": {
                    "tags": ["Pets"],
                    "summary": "Upload an image for a pet",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "pet_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                            "type": "string",
                            "format": "uuid"
                            },
                            "example": "0798602d-4e13-4e6a-9d89-1651ba2f59a6"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "required": ["image"],
                                    "properties": {
                                        "image": {
                                            "type": "string",
                                            "format": "binary",
                                            "description": "Pet image file"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Image uploaded",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ImageUploadResponse"}
                                }
                            }
                        },
                        "404": {"description": "Pet not found"}
                    }
                }
            }
        }
    })