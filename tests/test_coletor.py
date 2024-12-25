from src.coleta.coletor import Coletor


def test_status_code():

    coletor = Coletor()
    response = coletor.coleta_publicacoes(1, "20241220", "go", 8)
    assert response.status_code == 200


test_status_code()
