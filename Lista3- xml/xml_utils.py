import xml.etree.ElementTree as ET
from xml.dom import minidom
from models import Livro
from typing import List, Optional

XML_FILE = "livros.xml"

def salvar_livros(livros: List[Livro]):
    root = ET.Element("livros")
    for livro in livros:
        livro_el = ET.SubElement(root, "livro")
        for campo, valor in livro.dict().items():
            ET.SubElement(livro_el, campo).text = str(valor)
    tree = ET.ElementTree(root)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

     # Indentação para formatação do XML
    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(XML_FILE, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

def carregar_livros() -> List[Livro]:
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    except FileNotFoundError:
        return []
    
    livros = []
    for livro_el in root.findall("livro"):
        livro_data = {el.tag: el.text for el in livro_el}
        livro_data["id"] = int(livro_data["id"])
        livro_data["ano"] = int(livro_data["ano"])
        livros.append(Livro(**livro_data))
    return livros

def buscar_livro_por_id(livro_id: int) -> Optional[Livro]:
    livros = carregar_livros()
    for livro in livros:
        if livro.id == livro_id:
            return livro
    return None
