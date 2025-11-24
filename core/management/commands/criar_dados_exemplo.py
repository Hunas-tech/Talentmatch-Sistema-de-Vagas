from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Candidato, Empresa, Vaga, Match, Curso
from core.matching import calcular_compatibilidade
from decimal import Decimal


class Command(BaseCommand):
    help = 'Cria dados de exemplo para teste do sistema'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando dados de exemplo...')
        
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@talentmatch.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Admin criado: admin / admin123'))
        
        candidatos_data = [
            {
                'nome': 'João Silva',
                'email': 'joao@exemplo.com',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'habilidades': 'Python, Django, JavaScript, React, PostgreSQL',
                'experiencia_anos': 3,
                'escolaridade': 'Superior Completo',
                'area_interesse': 'Desenvolvimento Web',
                'pretensao_salarial': Decimal('5000.00'),
            },
            {
                'nome': 'Maria Santos',
                'email': 'maria@exemplo.com',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
                'habilidades': 'Java, Spring, MySQL, Docker, Kubernetes',
                'experiencia_anos': 5,
                'escolaridade': 'Superior Completo',
                'area_interesse': 'Backend',
                'pretensao_salarial': Decimal('7000.00'),
            },
            {
                'nome': 'Pedro Costa',
                'email': 'pedro@exemplo.com',
                'cidade': 'Belo Horizonte',
                'estado': 'MG',
                'habilidades': 'HTML, CSS, JavaScript, Vue.js, Figma',
                'experiencia_anos': 2,
                'escolaridade': 'Superior em Andamento',
                'area_interesse': 'Frontend',
                'pretensao_salarial': Decimal('4000.00'),
            },
        ]
        
        for candidato_data in candidatos_data:
            user, created = User.objects.get_or_create(
                email=candidato_data['email'],
                defaults={'username': candidato_data['email'].split('@')[0]}
            )
            if created:
                user.set_password('senha123')
                user.save()
            
            candidato, created = Candidato.objects.get_or_create(
                email=candidato_data['email'],
                defaults={**candidato_data, 'user': user}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Candidato criado: {candidato.nome}'))
        
        empresas_data = [
            {
                'nome': 'TechCorp Brasil',
                'cnpj': '12.345.678/0001-90',
                'email': 'contato@techcorp.com',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'setor': 'Tecnologia',
                'descricao': 'Empresa líder em soluções tecnológicas',
            },
            {
                'nome': 'Inovação Digital Ltda',
                'cnpj': '98.765.432/0001-10',
                'email': 'rh@inovacao.com',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
                'setor': 'Tecnologia',
                'descricao': 'Startup de transformação digital',
            },
        ]
        
        for empresa_data in empresas_data:
            user, created = User.objects.get_or_create(
                email=empresa_data['email'],
                defaults={'username': 'empresa_' + empresa_data['email'].split('@')[0]}
            )
            if created:
                user.set_password('senha123')
                user.save()
            
            empresa, created = Empresa.objects.get_or_create(
                cnpj=empresa_data['cnpj'],
                defaults={**empresa_data, 'user': user}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Empresa criada: {empresa.nome}'))
        
        empresas = Empresa.objects.all()
        if empresas.exists():
            vagas_data = [
                {
                    'titulo': 'Desenvolvedor Python Pleno',
                    'descricao': 'Buscamos desenvolvedor Python com experiência em Django',
                    'requisitos': 'Superior completo, experiência com APIs REST',
                    'habilidades_necessarias': 'Python, Django, PostgreSQL, Git',
                    'nivel': 'pleno',
                    'tipo': 'remoto',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'salario_min': Decimal('5000.00'),
                    'salario_max': Decimal('8000.00'),
                    'experiencia_minima': 3,
                },
                {
                    'titulo': 'Desenvolvedor Frontend React',
                    'descricao': 'Procuramos desenvolvedor frontend especializado em React',
                    'requisitos': 'Portfólio com projetos React',
                    'habilidades_necessarias': 'JavaScript, React, CSS, HTML',
                    'nivel': 'junior',
                    'tipo': 'hibrido',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'salario_min': Decimal('3500.00'),
                    'salario_max': Decimal('5500.00'),
                    'experiencia_minima': 1,
                },
                {
                    'titulo': 'Desenvolvedor Java Sênior',
                    'descricao': 'Vaga para desenvolvedor Java com experiência em microserviços',
                    'requisitos': 'Superior completo, certificações Java desejáveis',
                    'habilidades_necessarias': 'Java, Spring, Docker, Kubernetes, MySQL',
                    'nivel': 'senior',
                    'tipo': 'presencial',
                    'cidade': 'Rio de Janeiro',
                    'estado': 'RJ',
                    'salario_min': Decimal('8000.00'),
                    'salario_max': Decimal('12000.00'),
                    'experiencia_minima': 5,
                },
            ]
            
            for i, vaga_data in enumerate(vagas_data):
                empresa = empresas[i % empresas.count()]
                vaga, created = Vaga.objects.get_or_create(
                    titulo=vaga_data['titulo'],
                    empresa=empresa,
                    defaults=vaga_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Vaga criada: {vaga.titulo}'))
        
        cursos_data = [
            {
                'titulo': 'Python para Iniciantes',
                'descricao': 'Aprenda Python do zero',
                'categoria': 'Programação',
                'duracao_horas': 40,
                'nivel': 'Iniciante',
            },
            {
                'titulo': 'React Avançado',
                'descricao': 'Domine React e seus conceitos avançados',
                'categoria': 'Frontend',
                'duracao_horas': 60,
                'nivel': 'Avançado',
            },
            {
                'titulo': 'SQL e Banco de Dados',
                'descricao': 'Fundamentos de banco de dados relacionais',
                'categoria': 'Banco de Dados',
                'duracao_horas': 30,
                'nivel': 'Intermediário',
            },
        ]
        
        for curso_data in cursos_data:
            curso, created = Curso.objects.get_or_create(
                titulo=curso_data['titulo'],
                defaults=curso_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Curso criado: {curso.titulo}'))
        
        candidatos = Candidato.objects.all()
        vagas = Vaga.objects.all()
        matches_criados = 0
        
        for candidato in candidatos:
            for vaga in vagas:
                if not Match.objects.filter(candidato=candidato, vaga=vaga).exists():
                    score = calcular_compatibilidade(candidato, vaga)
                    if score >= 40:
                        Match.objects.create(
                            candidato=candidato,
                            vaga=vaga,
                            score=score
                        )
                        matches_criados += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {matches_criados} matches criados'))
        self.stdout.write(self.style.SUCCESS('\n✅ Dados de exemplo criados com sucesso!'))
        self.stdout.write('\nCredenciais de acesso:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Candidatos: joao@exemplo.com, maria@exemplo.com, pedro@exemplo.com / senha123')
        self.stdout.write('Empresas: contato@techcorp.com, rh@inovacao.com / senha123')
