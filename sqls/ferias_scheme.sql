
create schema ferias;

-- drop table ferias.upto25
create table ferias.upto25 (
	periodo1 integer,
	periodo2 integer,
	periodo3 integer
);

-- drop table ferias.opcao_ferias;
create table ferias.opcao_ferias ( 
	dt_oficial_inicial date,
	dt_oficial_final date,
    dt_real_inicial date,
	dt_real_final date,
	tamanho integer,
    dias_corridos_oficiais integer, 
	dias_corridos_reais integer, 
	dias_uteis_oficiais integer, 
	dias_uteis_reais integer,
	dias_corridos_esperados integer, 
	alavancagem integer
);
create index opcao_ferias_tamanho on ferias.opcao_ferias (tamanho);
create index opcao_ferias_dias_corridos_reais on ferias.opcao_ferias (dias_corridos_reais);
create index opcao_ferias_dt_oficial_inicial on ferias.opcao_ferias (dt_oficial_inicial);


-- drop table ferias.eventos_calendario
create table ferias.eventos_calendario (
	id integer, 
	descricao text
);

-- drop table ferias.calendario
create table ferias.calendario (
	tipo integer, 
	dt_dia date, 
	descricao text
);



