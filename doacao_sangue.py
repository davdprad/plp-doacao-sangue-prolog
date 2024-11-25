from pyswip import Prolog

class DoacaoSangue:
    def __init__(self, prolog_file):
        self.prolog = Prolog()
        self.load_prolog_file(prolog_file)

    def load_prolog_file(self, prolog_file):
        """
        Carregar o arquivo Prolog com a base de conhecimento e regras
        """
        self.prolog.consult(prolog_file)

    def verificar_compatibilidade(self, doador, receptor):
        """
        Verificar se um doador pode doar sangue para um receptor
        """
        query = f"podedoar({doador}, {receptor})"
        result = list(self.prolog.query(query))
        print(result)
        return bool(result)

    def consultar_tipo_sanguineo(self, pessoa):
        """
        Consultar o tipo sanguíneo de uma pessoa
        """
        query = f"tiposanguineo({pessoa}, Tipo)"
        result = list(self.prolog.query(query))
        if result:
            return result[0]["Tipo"]
        return None

    def consultar_fator_rh(self, pessoa):
        """
        Consultar o fator RH de uma pessoa
        """
        query = f"fatorrh({pessoa}, RH)"
        result = list(self.prolog.query(query))
        if result:
            return result[0]["RH"]
        return None

    def consultar_aptos(self):
        """
        Consultar o fator RH de uma pessoa
        """
        query = f"quem_pode_doar(DoadoresUnicos)"
        result = list(self.prolog.query(query))
        if result:
            return result[0]['DoadoresUnicos']
        return None
    
    def consultar_doar_receber(self, pessoa):
        """
        Consultar o fator RH de uma pessoa
        """
        query = f"pode_doar_receber({pessoa}, ListaUnica)"
        result = list(self.prolog.query(query))
        if result:
            return result[0]['ListaUnica']
        return None
    
    def quem_possui_tipo(self, tipo):
        """
        Consultar o fator RH de uma pessoa
        """
        query = f"quem_possui_tipo({tipo}, Pessoas)"
        result = list(self.prolog.query(query))
        if result:
            return result[0]['Pessoas']
        return None
    
    def quem_possui_fator(self, fator):
        """
        Consultar o fator RH de uma pessoa
        """
        query = f"quem_tem_fator_rh({fator}, Pessoas)"
        result = list(self.prolog.query(query))
        if result:
            return result[0]['Pessoas']
        return None
