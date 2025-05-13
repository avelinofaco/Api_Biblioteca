import csv
import xml.etree.ElementTree as ET

def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def csv_xml(caminho_csv, nome_base, caminho_xml):
    
    with open(caminho_csv, newline='', encoding='utf-8') as f:
            
        leitor = csv.DictReader(f)
        root = ET.Element(nome_base)

        for linha in leitor:
            item_elem = ET.SubElement(root, nome_base[:-1] if nome_base.endswith('s') else 'item')
            for chave, valor in linha.items():
                ET.SubElement(item_elem, chave).text = valor

        tree = ET.ElementTree(root)
        indent(root)
        tree.write(caminho_xml, encoding='utf-8', xml_declaration=True)
        
    return True