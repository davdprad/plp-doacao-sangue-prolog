import wx
from doacao_sangue import DoacaoSangue
from functools import reduce

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.sistema = DoacaoSangue("doacao_sangue.pl")
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Título
        title = wx.StaticText(panel, label="Sistema de Doação de Sangue")
        vbox.Add(title, flag=wx.EXPAND | wx.TOP, border=20)

        # Campo de entrada para doador e receptor =====================================================

        self.doador_input = wx.TextCtrl(panel, size=(200, 25))
        self.receptor_input = wx.TextCtrl(panel, size=(200, 25))
        vbox.Add(wx.StaticText(panel, label="Doador:"), flag=wx.TOP, border=10)
        vbox.Add(self.doador_input, flag=wx.TOP, border=5)
        vbox.Add(wx.StaticText(panel, label="Receptor:"), flag=wx.TOP, border=10)
        vbox.Add(self.receptor_input, flag=wx.TOP, border=5)

        # Botão para verificar compatibilidade
        check_button = wx.Button(panel, label="Verificar Compatibilidade")
        check_button.Bind(wx.EVT_BUTTON, self.on_check_compatibility)
        vbox.Add(check_button, flag=wx.TOP | wx.EXPAND, border=10)

        # Resultados
        self.result_text = wx.TextCtrl(panel, size=(200, 50), style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.result_text, flag=wx.TOP | wx.EXPAND, border=10)

        # Consultas ===================================================================================

        self.consulta_input = wx.TextCtrl(panel, size=(200, 25))
        vbox.Add(wx.StaticText(panel, label="Consultar:"), flag=wx.TOP, border=10)
        vbox.Add(self.consulta_input, flag=wx.TOP, border=5)

        # Consultar tipo sanguíneo e fator RH
        consult_panel0 = wx.BoxSizer(wx.HORIZONTAL)
        self.consultar_button = wx.Button(panel, label="Consultar Tipo Sanguíneo")
        self.consultar_button.Bind(wx.EVT_BUTTON, self.on_consultar_tipo_sanguineo)
        consult_panel0.Add(self.consultar_button, flag=wx.RIGHT, border=10)
        self.consultar_rh_button = wx.Button(panel, label="Consultar Fator RH")
        self.consultar_rh_button.Bind(wx.EVT_BUTTON, self.on_consultar_fator_rh)
        consult_panel0.Add(self.consultar_rh_button)
        vbox.Add(consult_panel0, flag=wx.TOP | wx.EXPAND, border=20)

        # Consultar quem está apto e quem pode doar e receber de alguém
        consult_panel1 = wx.BoxSizer(wx.HORIZONTAL)
        self.aptos_button = wx.Button(panel, label="Quem está apto?")
        self.aptos_button.Bind(wx.EVT_BUTTON, self.consultar_aptos)
        consult_panel1.Add(self.aptos_button, flag=wx.RIGHT, border=10)
        self.aptos_button = wx.Button(panel, label="Para quem pode doar ou receber?")
        self.aptos_button.Bind(wx.EVT_BUTTON, self.consultar_doar_receber)
        consult_panel1.Add(self.aptos_button, flag=wx.RIGHT, border=10)
        vbox.Add(consult_panel1, flag=wx.TOP | wx.EXPAND, border=20)

        # Consultar quem está apto e quem pode doar e receber de alguém
        consult_panel3 = wx.BoxSizer(wx.HORIZONTAL)
        self.tipo_button = wx.Button(panel, label="Quem possui tipo sanguíneo?")
        self.tipo_button.Bind(wx.EVT_BUTTON, self.quem_possui_tipo)
        consult_panel3.Add(self.tipo_button, flag=wx.RIGHT, border=10)
        self.fator_button = wx.Button(panel, label="Quem possui fator rh?")
        self.fator_button.Bind(wx.EVT_BUTTON, self.quem_possui_fator)
        consult_panel3.Add(self.fator_button, flag=wx.RIGHT, border=10)
        vbox.Add(consult_panel3, flag=wx.TOP | wx.EXPAND, border=20)

        # Resultados para consultas
        self.result_consulta = wx.TextCtrl(panel, size=(200, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.result_consulta, flag=wx.TOP | wx.EXPAND, border=10)

        panel.SetSizer(vbox)
        self.SetSize((400, 700))
        self.SetTitle("Sistema de Doação de Sangue")
        self.Centre()

    def on_check_compatibility(self, event):
        doador = self.doador_input.GetValue().strip()
        receptor = self.receptor_input.GetValue().strip()

        if doador and receptor:
            if self.sistema.verificar_compatibilidade(doador, receptor):
                result = f"{doador} pode doar sangue para {receptor}."
            else:
                result = f"{doador} não pode doar sangue para {receptor}."
            self.result_text.SetValue(result)
        else:
            self.result_text.SetValue("Por favor, insira o nome do doador e receptor.")

    def on_consultar_tipo_sanguineo(self, event):
        pessoa = self.consulta_input.GetValue().strip()
        if pessoa:
            tipo = self.sistema.consultar_tipo_sanguineo(pessoa)
            if tipo:
                self.result_consulta.SetValue(f"{pessoa} possui o tipo sanguíneo {tipo}.")
            else:
                self.result_consulta.SetValue(f"Tipo sanguíneo de {pessoa} não encontrado.")
        else:
            self.result_consulta.SetValue("Por favor, insira o nome da pessoa.")

    def on_consultar_fator_rh(self, event):
        pessoa = self.consulta_input.GetValue().strip()
        if pessoa:
            rh = self.sistema.consultar_fator_rh(pessoa)
            if rh:
                self.result_consulta.SetValue(f"{pessoa} possui o fator RH {rh}.")
            else:
                self.result_consulta.SetValue(f"Fator RH de {pessoa} não encontrado.")
        else:
            self.result_consulta.SetValue("Por favor, insira o nome da pessoa.")

    def consultar_aptos(self, event):
        aptos_list = self.sistema.consultar_aptos()
        if aptos_list:
            aptos = reduce(lambda x, y: x + "\n - " + y, aptos_list, "")
            self.result_consulta.SetValue(f"Todos que estão aptos para doar:{aptos}")
        else:
            self.result_consulta.SetValue(f"Não há aptos.")

    def consultar_doar_receber(self, event):
        pessoa = self.consulta_input.GetValue().strip()
        if pessoa:
            lista = self.sistema.consultar_doar_receber(pessoa)
            if lista:
                resp = reduce(lambda x, y: x + "\n - " + y, lista, "")
                self.result_consulta.SetValue(f"Todos que podem doar e receber para {pessoa}:{resp}")
            else:
                self.result_consulta.SetValue(f"Não há quem doar ou receber para {pessoa}.")
        else: 
            self.result_consulta.SetValue("Por favor, insira o nome da pessoa.")

    def quem_possui_tipo(self, event):
        tipo = self.consulta_input.GetValue().strip()
        if tipo:
            lista = self.sistema.quem_possui_tipo(tipo)
            if lista:
                resp = reduce(lambda x, y: x + "\n - " + y, lista, "")
                self.result_consulta.SetValue(f"Todos que possuem o tipo {tipo}:{resp}")
            else:
                self.result_consulta.SetValue(f"Não há pessoas com esse tipo.")
        else: 
            self.result_consulta.SetValue("Por favor, insira o tipo.")

    def quem_possui_fator(self, event):
        fator = self.consulta_input.GetValue().strip()
        if fator:
            lista = self.sistema.quem_possui_fator(fator)
            if lista:
                resp = reduce(lambda x, y: x + "\n - " + y, lista, "")
                self.result_consulta.SetValue(f"Todos que possuem o fator rh {fator}:{resp}")
            else:
                self.result_consulta.SetValue(f"Não há pessoas com esse fator rh.")
        else: 
            self.result_consulta.SetValue("Por favor, insira o fator.")
