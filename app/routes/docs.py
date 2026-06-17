from flask import Blueprint, jsonify, Response, current_app, redirect

docs_bp = Blueprint("docs", __name__)


@docs_bp.get("/docs")
def docs_redirect():
    return redirect("/docs/", code=301)


@docs_bp.get("/docs/")
def swagger_ui():
    client_id = current_app.config.get("AUTH0_CLIENT_ID")

    return Response(f"""
<!DOCTYPE html>
<html>
<head>
  <title>PetFlow API • Swagger</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  <style>
    body {{
      margin: 0;
      background: #fafafa;
    }}
    .topbar {{
      display: none;
    }}
  </style>
</head>
<body>
  <div id="swagger-ui"></div>

  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>

  <script>
    window.onload = function() {{
      const ui = SwaggerUIBundle({{
        url: window.location.origin + "/openapi.json",
        dom_id: "#swagger-ui",
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        deepLinking: true,
        persistAuthorization: true,
        displayRequestDuration: true,
        filter: true,
        oauth2RedirectUrl: window.location.origin + "/docs/oauth2-redirect.html"
      }});

      ui.initOAuth({{
        clientId: "{client_id}",
        usePkceWithAuthorizationCodeGrant: true,
        scopes: "openid profile email"
      }});

      window.ui = ui;
    }};
  </script>
</body>
</html>
""", mimetype="text/html")

@docs_bp.get("/docs/oauth2-redirect.html")
def oauth2_redirect():
    return Response("""
<!doctype html>
<html lang="en-US">
<head>
    <title>Swagger UI: OAuth2 Redirect</title>
</head>
<body>
<script>
'use strict';
function run () {
    var oauth2 = window.opener.swaggerUIRedirectOauth2;
    var sentState = oauth2.state;
    var redirectUrl = oauth2.redirectUrl;
    var isValid, qp, arr;

    if (/code|token|error/.test(window.location.hash)) {
        qp = window.location.hash.substring(1).replace('?', '&').split('&');
    } else {
        qp = location.search.substring(1).split('&');
    }

    arr = qp.map(function (v) {
        var p = v.split('=');
        var key = decodeURIComponent(p[0]);
        var value = p[1] ? decodeURIComponent(p[1]) : '';
        return [key, value];
    });

    arr.forEach(function (v) {
        if (v[0] === 'state') {
            isValid = v[1] === sentState;
        }
    });

    if (!isValid) {
        oauth2.errCb({
            authId: oauth2.auth.name,
            source: 'auth',
            level: 'warning',
            message: 'Authorization may be unsafe, passed state was changed in server. The passed state wasn\\'t returned from auth server.'
        });
    }

    if (oauth2.auth.schema.get('flow') === 'accessCode' ||
        oauth2.auth.schema.get('flow') === 'authorizationCode' ||
        oauth2.auth.schema.get('flow') === 'authorization_code') {
        oauth2.auth.code = arr.filter(function (v) {
            return v[0] === 'code';
        }).map(function (v) {
            return v[1];
        })[0];

        oauth2.callback({auth: oauth2.auth, redirectUrl: redirectUrl});
    } else {
        oauth2.callback({auth: oauth2.auth, token: arr, isValid: isValid, redirectUrl: redirectUrl});
    }
}
window.onload = run;
</script>
</body>
</html>
""", mimetype="text/html")

@docs_bp.get("/openapi.json")
def openapi():
    auth0_domain = current_app.config.get("AUTH0_DOMAIN")
    auth0_audience = current_app.config.get("AUTH0_AUDIENCE")
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
                "Auth0": {
                    "type": "oauth2",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": f"https://{auth0_domain}/authorize?audience={auth0_audience}",
                            "tokenUrl": f"https://{auth0_domain}/oauth/token",
                            "scopes": {
                                "openid": "OpenID Connect",
                                "profile": "User profile",
                                "email": "User email"
                            }
                        }
                    }
                },

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
                    "required": ["name", "species" ],
                    "properties": {
                        "name": {"type": "string", "example": "Leyn"},
                        "species": {"type": "string", "example": "Dog"},
                        "breed": {"type": "string", "nullable": True, "example": "Mixed"},
                        "gender": {"type": "string", "nullable": True, "example": "Female"},
                        "age": {"type": "integer", "nullable": True, "example": 8},
                        "color": {"type": "string", "nullable": True, "example": "Brown"},
                        "description": {"type": "string", "nullable": True, "example": "Friendly dog"},
                        "chip_number": {"type": "string", "nullable": True, "example": "985141000123456"}
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
            "/auth0/me": {
                "get": {
                    "tags": ["Authentication"],
                    "summary": "Validate Auth0 token",
                    "security": [{"Auth0": ["openid", "profile", "email"]}],
                    "responses": {
                        "200": {
                            "description": "Auth0 token is valid"
                        },
                        "401": {
                            "description": "Invalid Auth0 token"
                        }
                    }
                }
            },
            "/me": {
                "get": {
                    "tags": ["Authentication"],
                    "summary": "Get current authenticated user",
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
                    "responses": {
                        "200": {
                            "description": "Current user details"
                        },
                        "401": {
                            "description": "Unauthorized"
                        }
                    }
                }
            },
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
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
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
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
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
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
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
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
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
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
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
                    "security": [
                        {"Auth0": ["openid", "profile", "email"]},
                        {"BearerAuth": []}
                    ],
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
                                    "required": ["file"],
                                    "properties": {
                                        "file": {
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