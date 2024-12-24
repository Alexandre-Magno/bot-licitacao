from src.coleta.coletor import Coletor


def test_status_code():
    coletor = Coletor()
    response = coletor.coleta_publicacoes()
    assert response.status_code == 200
