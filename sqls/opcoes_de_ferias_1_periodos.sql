
With oferias As (
	Select * From ferias.opcao_ferias ofe
	Where ofe.alavancagem >= 1
		And ofe.dt_oficial_inicial Between ':ano:-01-01' And ':ano:-12-31'
)

Select
	/* primeiro periodo de ferias */
	f1.dt_real_inicial As p1_inicio_real, 
 	f1.dt_oficial_inicial As p1_inicio_oficial, 
	f1.dt_oficial_final As p1_fim_oficial, 
	f1.dt_real_final As p1_fim_real, 
	f1.tamanho As p1_tamanho, 
	f1.dias_corridos_reais As p1_aproveitados,


	/* resultado geral */
	( f1.dias_corridos_reais ) As reais,
	( f1.dias_corridos_esperados ) As esperados

From oferias f1
Where f1.dias_corridos_reais >= :minimo_dias_corridos_reais:


Order By reais Desc, f1.dt_oficial_inicial

Limit :limit:


/*

Host: 10.27.10.238
Port: 5432
Database: pessoal
User: postgres
Password: postgres

Postgresql URL: jdbc:postgresql://10.27.10.238:5432/pessoal

*/

