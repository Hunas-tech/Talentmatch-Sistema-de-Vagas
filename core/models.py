from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=50, blank=True)
    pronomes = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    pcd = models.BooleanField(default=False)
    
    habilidades = models.TextField(blank=True, help_text="Habilidades separadas por vírgula")
    experiencia_anos = models.IntegerField(default=0)
    escolaridade = models.CharField(max_length=100, blank=True)
    area_interesse = models.CharField(max_length=200, blank=True)
    pretensao_salarial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    curriculo = models.TextField(blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Candidatos"
    
    def __str__(self):
        return self.nome


class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=300, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    setor = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(blank=True)
    site = models.URLField(blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Empresas"
    
    def __str__(self):
        return self.nome


class Vaga(models.Model):
    NIVEL_CHOICES = [
        ('estagio', 'Estágio'),
        ('junior', 'Júnior'),
        ('pleno', 'Pleno'),
        ('senior', 'Sênior'),
    ]
    
    TIPO_CHOICES = [
        ('remoto', 'Remoto'),
        ('presencial', 'Presencial'),
        ('hibrido', 'Híbrido'),
    ]
    
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
        ('pausada', 'Pausada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    requisitos = models.TextField(help_text="Requisitos da vaga")
    habilidades_necessarias = models.TextField(help_text="Habilidades separadas por vírgula")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experiencia_minima = models.IntegerField(default=0, help_text="Anos de experiência")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Vagas"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome}"


class Match(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
        ('entrevista', 'Em Entrevista'),
        ('contratado', 'Contratado'),
    ]
    
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='matches')
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='matches')
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score de compatibilidade (0-100)"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    candidato_interessado = models.BooleanField(default=False)
    empresa_interessada = models.BooleanField(default=False)
    
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Matches"
        unique_together = ['candidato', 'vaga']
        ordering = ['-score', '-criado_em']
    
    def __str__(self):
        return f"Match: {self.candidato.nome} - {self.vaga.titulo} ({self.score}%)"


class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    assunto = models.CharField(max_length=200)
    conteudo = models.TextField()
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Mensagens"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.remetente.username} -> {self.destinatario.username}: {self.assunto}"


class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    duracao_horas = models.IntegerField()
    nivel = models.CharField(max_length=50)
    conteudo = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Cursos"
    
    def __str__(self):
        return self.titulo


class ProgressoCurso(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='cursos_progresso')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    progresso = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    concluido = models.BooleanField(default=False)
    iniciado_em = models.DateTimeField(auto_now_add=True)
    concluido_em = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Progressos de Cursos"
        unique_together = ['candidato', 'curso']
    
    def __str__(self):
        return f"{self.candidato.nome} - {self.curso.titulo} ({self.progresso}%)"
