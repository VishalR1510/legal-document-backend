#!/usr/bin/env python3
"""
Test script to verify backend setup
"""
import sys
print("=" * 60)
print("BACKEND DIAGNOSTICS")
print("=" * 60)

# Test 1: NumPy version
print("\n[1] Checking NumPy version...")
try:
    import numpy
    numpy_version = numpy.__version__
    numpy_major = int(numpy_version.split('.')[0])
    print(f"    ✓ NumPy {numpy_version}")
    if numpy_major >= 2:
        print("    ✗ NumPy 2.x detected - may cause issues")
        print("     RUN: pip install 'numpy<2'")
    else:
        print("    ✓ NumPy 1.x - compatible")
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 2: Config loading
print("\n[2] Loading configuration...")
try:
    from app.core.config import settings
    print(f"    ✓ Project: {settings.PROJECT_NAME}")
    print(f"    ✓ API Key: {'SET' if settings.GEMINI_API_KEY else 'NOT SET'}")
except Exception as e:
    print(f"    ✗ Error loading config: {e}")

# Test 3: Embedding service
print("\n[3] Testing Embedding Service...")
try:
    from app.services.embedding_service import embedding_service
    embedding = embedding_service.generate_embedding("test")
    print(f"    ✓ Embedding generated (vector size: {len(embedding)})")
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 4: Qdrant service
print("\n[4] Testing Qdrant Service...")
try:
    from app.services.qdrant_service import qdrant_service
    print(f"    ✓ Qdrant initialized")
    collections = qdrant_service.client.get_collections()
    print(f"    ✓ Collections: {[c.name for c in collections.collections]}")
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 5: RAG service
print("\n[5] Testing RAG Service...")
try:
    from app.services.rag_service import rag_service
    print(f"    ✓ RAG service initialized")
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 6: FastAPI app
print("\n[6] Loading FastAPI App...")
try:
    from main import app
    print(f"    ✓ FastAPI app loaded")
    print(f"    ✓ Routes:")
    for route in app.routes:
        print(f"      - {route.path}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)
