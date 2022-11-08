.PHONY: notebook docs     # Define que o arquivo make vai rodar as rotinas independente dos arquivos e modificações
.EXPORT_ALL_VARIABLES:    # Passa todas as variáveis do arquivo Make para os submakes 


## Instalar as dependências Poetry e rodar o script de plugins pre-commit
install: 
	@echo "Installing..."
	poetry install    
	poetry run pre-commit install

## Iniciar os ambiente virtual
activate:
	@echo "Activating virtual environment"
	poetry shell    

## Iniciar o repositório local Git
initialize_git:
	git init     

## Rodar o script DVC para carregar os dados
pull_data:
	@echo "Pulling data..."
	poetry run dvc pull -r origin

## Rodar as ro tinas de repositório git e instalar dependência dos sistema
setup: initialize_git install 

## Adiciona as pastas data e model para o tracker do dvc
dvc_add:
	dvc add data model

## Carregar os arquivos locais para o repositório remoto dvc (dagshub)
dvc_push:
	dvc push -r origin

## Adiciona todos os arquivos à área de stage e mostra os status do repositório local git
git_add:
	git add .
	git status

add: dvc_add dvc_push git_add

## Ativar pytest
test:
	pytest    

## Abrir a documentação API na porta local padrão
docs_view:
	@echo View API documentation... 
	pdoc src --http localhost:8080     

## Salvar documentação API automatizada
docs_save:
	@echo Save documentation to docs... 
	pdoc src -o docs     

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
