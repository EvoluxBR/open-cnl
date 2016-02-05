from open_cnl.open_cnl import OpenCNLImporter

cnl_importer = OpenCNLImporter('./dist/base.txt', './dist/banco.sqlite3')
cnl_importer.importar_base()
