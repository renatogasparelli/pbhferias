
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

	/* segundo periodo de ferias */
	f2.dt_real_inicial As p2_inicio_real, 
	f2.dt_oficial_inicial As p2_inicio_oficial, 
	f2.dt_oficial_final As p2_fim_oficial, 
	f2.dt_real_final As p2_fim_real, 
	f2.tamanho As p2_tamanho, 
	f2.dias_corridos_reais As p2_aproveitados,


	/* resultado geral */
	( f1.dias_corridos_reais + f2.dias_corridos_reais ) As reais,
	( f1.dias_corridos_esperados + f2.dias_corridos_esperados ) As esperados

From ferias.upto25 up2
	inner join oferias f1 on f1.tamanho = up2.periodo1
	inner join oferias f2 on f2.tamanho = up2.periodo2
		And f2.dt_real_inicial  > f1.dt_real_final


Where   ( f1.dias_corridos_reais + f2.dias_corridos_reais ) >= :minimo_dias_corridos_reais:
	And ( f1.dias_corridos_reais + f2.dias_corridos_reais ) > ( f1.dias_corridos_esperados + f2.dias_corridos_esperados )
	And ( up2.periodo3 = 0 )
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

