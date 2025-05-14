#!/usr/bin/env python3
import os
import sys

# Asegúrate de que Python encuentre tu carpeta `app`
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.services.superbid_service import import_superbid_auctions

if __name__ == "__main__":
    import_superbid_auctions()
    print("Importación de Superbid completada.")
