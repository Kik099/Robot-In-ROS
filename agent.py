#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by:Rodrigo Saraiva a39441
import datetime
import rospy
from decimal import Decimal
from decimal import ROUND_HALF_UP
import copy
import networkx as nx
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''
sala_ant = "Elevador 0"
lista = []
suites = []

visitadas = []
tempo=datetime.datetime.now()
G=nx.complete_graph(1)


#--------------------------------------------------------------
def local(x,y):
	
	if ((x>=-15.7 and x<=3.5) and (y>=-3.1 and y<=-1.4)):
		return "Corredor 1"
	elif ((x>=-15.7 and x<=-12) and (y>=-1.1 and y<=2.8)):
		return "Room 5"
	elif ((x>=-15.7 and x<=-12) and (y>=2.8 and y<=7.3)):
		return "Room 6"
	elif ((x>=-15.7 and x<=-11.2) and (y>=8.0 and y<=11.1)):
		return "Room 7"
	elif ((x>=-10.6 and x<=-6.2) and (y>=8.0 and y<=11.1)):
		return "Room 8"
	elif ((x>=-11.8 and x<=-9.2) and (y>=-1.1 and y<=5.3)):
		return "Corredor 2"
	elif ((x>=-4 and x<=-1.4) and (y>-1.4 and y<5.5)):
		return "Corredor 4"
	elif ((x>=-11.8 and x<=3.6) and (y>=5.2 and y<=7.3)):
		return "Corredor 3"
	elif ((x>=-9.2 and x<=-6.9) and (y>=-0.9 and y<=5.0)):
		return "Room 13"
	elif ((x>=-6.6 and x<=-4.5) and (y>=-0.9 and y<=5.0)):
		return "Room 14"
	elif ((x>=-1.0 and x<=3.5) and (y>=2.2 and y<=5.0)):
		return "Room 11"
	elif ((x>=-1.0 and x<=3.5) and (y>=-1.1 and y<=2.0)):
		return "Room 12"
	elif ((x>=-5.7 and x<=-1.1) and (y>=7.9 and y<=11)):
		return "Room 9"
	elif ((x>=-0.6 and x<=3.5) and (y>=7.9 and y<=11)):
		return "Room 10"
	else:
		return "Porta"
	
# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, visitadas,sala_ant,G
	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		sala=local(x,y)
		
		if sala_ant != sala and sala != "Porta":
			print "Sala: %s" %sala
			roomTipo(x,y)
			G.add_edge(int(sala_ant.split(" ")[1]),int(sala.split(" ")[1]))
			if sala not in visitadas:
				visitadas.append(sala)
				

			sala_ant = sala	


	x_ant = x
	y_ant = y
	
# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant,lista,x_ant,y_ant
	obj = data.data
	if obj != obj_ant and data.data != "":
		print "object is %s" % data.data
		obj_ant = obj
		list_ob=obj.split(',')#separar os objetos pela delimitação da virgula  e guarda-se na lista list_obj
		for i in range(len(list_ob)):
			add=(list_ob[i],local(x_ant,y_ant))		#o add toma um objeto e o local onde este foi encontrado
			if add not in lista:
				lista.append(add)#caso o add não esteja na lista, acrescenta-se esse mesmo


def Pergunta6():
	global x_ant,y_ant

	roomAtual = local(x_ant, y_ant)
	source = int(local(x_ant, y_ant).split(" ")[1])
		#procurar o menor caminho dos possíveis entre a sala onde estou e a sala 5
	path = nx.shortest_path(G, source,target = 0)
	
	print"Caminho mais rapido"	
	for i in range(len(path)):
		if "1" == str(path[i]):
			print "Corredor 1"
		elif "2" == str(path[i]):
			print "Corredor 2"
		elif "3" == str(path[i]):
			print "Corredor 3"
		elif "4" == str(path[i]):
			print "Corredor 4"
		elif "5" == str(path[i]):
			print "Room 5"
		elif "6" == str(path[i]):
			print "Room 6"
		elif "7" == str(path[i]):
			print "Room 7"
		elif "8" == str(path[i]):
			print "Room 8"
		elif "9" == str(path[i]):
			print "Room 9"
		elif "10" == str(path[i]):
			print "Room 10"			
		elif "11" == str(path[i]):
			print "Room 11"		
		elif "12" == str(path[i]):
			print "Room 12"
		elif "13" == str(path[i]):
			print "Room 13"
		elif "14" == str(path[i]):
			print "Room 14"
		elif "0" == str(path[i]):
			print "Elevador"
#--------------------------------------------------------------
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	global lista
	print "question is %s" % data.data
	es=data.data
	if(es=="1"):

		Pergunta1()
	elif(es=="2"):
		Pergunta2()
	elif(es=="3"):
		Pergunta3()
	elif(es=="4"):
		Pergunta4()	
	elif(es=="5"):
		Pergunta5()
	elif(es=="6"):
		Pergunta6()
	elif(es=="7"):
		Pergunta7()
	elif(es=="8"):
		Pergunta8()

def Pergunta7():
	
	
	book=0
	#contar o numero de livros encontrados ate ao momento
	for i in range(len(lista)):
		obj=str(lista[i][0])
		if "book" in obj:
			book+=1
	#vamos criar a variavel temp para obtermos o tempo atual, menos o tempo em que o programa foi iniciado
	#a biblioteca datetime.now da as horas em que a linha de baixo é corrida
	temp=datetime.datetime.now()-tempo
	temp=temp.total_seconds()
	#vamos multiplicar o numero de livros vistos ate ao momento por 2 minutos(120 seg)
	#dividindo pelo tempo atual do programa( desde que foi iniciado ate ao momento)
	Estimativa=(book*120)/temp
	#arredondar para o float para inteiro de acordo com as suas casas decimais
	arredondado= Decimal(Estimativa).quantize(0, ROUND_HALF_UP)
	print arredondado
	

def Pergunta8():
	global visitadas,x_ant,y_ant
	aux=0 #vai guardar o numero de quartos em que existe pelo menos uma cadeira
	aux2=0 # vai guardar os quartos que tem pelo menos uma cadeira, onde nao
	       # existam livros e onde existam mesas
	obj_room=[]
	vis=copy.copy(visitadas)
	#remover corredores da lista de visitadas criada para esta funcao
	if "Corredor 2" in vis:
		vis.remove("Corredor 2")
	if "Corredor 1" in vis:
		vis.remove("Corredor 1")
	if "Corredor 3" in vis:
		vis.remove("Corredor 3")
	if "Corredor 4" in vis:
		vis.remove("Corredor 4")
	if int(len(vis))==0:
		print"Nao temos informção suficiente, nenhum quarto visitado ate ao momento"
	else:
		for x in range(len(vis)):
			chair=0
			table=0
			book=0		
			obj_room=objectRoom(vis[x])
			if int(len(obj_room))>0:
		
				for i in range(len(obj_room)):
					if "chair" in obj_room[i]:
						chair += 1
					if "table" in obj_room[i]:
						table += 1
					if "book" in obj_room[i]:
						book += 1
				if chair >0:
					aux += 1
				if chair >0 and table > 0 and book==0:
					aux2 += 1
			
		if aux==0:
			print "Ainda nao foram encontrados quartos com pelo menos uma cadeira"
		else:
			print "%.2f" %(float(aux2)/float(aux))
			
		
		
	
		

	

def Pergunta2():
	global suites
	aux=0
	if len(suites)!=0:
		print "room type(s):"
		for i in range(len(suites)):
			print suites[i]
	else:
		print"Pelos dados lidos ate ao momento ainda nao foi visto nenhuma suite"
	
def Pergunta1():
	global lista,visitadas
	room5=0
	room6=0
	room7=0
	room8=0
	room9=0
	room10=0
	room11=0
	room12=0
	room13=0
	room14=0
	aux=[]
	aux2=[]

	aux=copy.copy(visitadas)
	if "Corredor 2" in aux:
		aux.remove("Corredor 2")
	if "Corredor 1" in aux:
		aux.remove("Corredor 1")
	if "Corredor 3" in aux:
		aux.remove("Corredor 3")
	if "Corredor 4" in aux:
		aux.remove("Corredor 4")			 		
								
	for i in range(len(lista)):
        #vamos verificar na lista se existem pessoas, caso existam vamos remover da lista aux o quarto correspondente
		if "person_" in lista[i][0] and "Room 5" in lista[i][1] and room5==0 and "Room 5" in aux:
			room5+=1
			aux.remove("Room 5")
		elif "person_" in lista[i][0] and "Room 6" in lista[i][1] and room6==0 and "Room 6" in aux:
			room6+=1	
			aux.remove("Room 6")
			
		elif "person_" in lista[i][0] and "Room 7" in lista[i][1] and room7==0 and "Room 7" in aux:
			room7+=1
			aux.remove("Room 7")	
		elif "person_" in lista[i][0] and "Room 8" in lista[i][1] and room8==0 and "Room 8" in aux:
			room8+=1
			aux.remove("Room 8")
		elif "person_" in lista[i][0] and "Room 9" in lista[i][1] and room9==0 and "Room 9" in aux:
			room9+=1
			aux.remove("Room 9")
		elif "person_" in lista[i][0] and "Room 10" in lista[i][1] and room10==0 and "Room 10" in aux:
			room10+=1
			aux.remove("Room 10")
		elif "person_" in lista[i][0] and "Room 11" in lista[i][1] and room11==0 and "Room 11" in aux:
			room11+=1
			aux.remove("Room 11")
		elif "person_" in lista[i][0] and "Room 12" in lista[i][1] and room12==0 and "Room 12" in aux:
			room12+=1
			aux.remove("Room 12")
		elif "person_" in lista[i][0] and "Room 13" in lista[i][1] and room13==0 and "Room 13" in aux:
			room13+=1
			aux.remove("Room 13")
		elif "person_" in lista[i][0] and "Room 14" in lista[i][1] and room14==0 and "Room 14" in aux:
			room14+=1
			aux.remove("Room 14")
	aux2=copy.copy(visitadas)
	if "Corredor 2" in aux2:
		aux2.remove("Corredor 2")
	if "Corredor 1" in aux2:
		aux2.remove("Corredor 1")
	if "Corredor 3" in aux2:
		aux2.remove("Corredor 3")
	if "Corredor 4" in aux2:
		aux2.remove("Corredor 4")			 		
					
	
#vai ser dada a informação dos quartos que vimos ate ao momento e os quartos livres
	print "quartos visitadas ate ao momento: %d "  %len(aux2) 
	print "quartos livres: %d" %len(aux)

def Pergunta3():
	global lista
	global visitadas

		
	
	nSP = 0 #número de quartos com pessoas
	nCP = 0 #número de corredores com pessoas
	rooms = []
	NSP=[]	#número de quartos visitados
	NCP=[]  ##número de Corredores visitados
	NSP=copy.copy(visitadas)
    #vai se remover os corredores para serem só os quartos na lista NSP
	if "Corredor 2" in NSP:
		NSP.remove("Corredor 2")
	if "Corredor 1" in NSP:
		NSP.remove("Corredor 1")
	if "Corredor 3" in NSP:
		NSP.remove("Corredor 3")
	if "Corredor 4" in NSP:
		NSP.remove("Corredor 4")

	NCP=copy.copy(visitadas)
	
    #vai se remover os quartos para serem só os corredores na lista NCP
	
	if "Room 5" in NCP:
		NCP.remove("Room 5")
	if "Room 6" in NCP:
			NCP.remove("Room 6")
	if "Room 7" in NCP:
			NCP.remove("Room 7")
	if "Room 8" in NCP:
			NCP.remove("Room 8")
	if "Room 9" in NCP:
			NCP.remove("Room 9 ")
	if "Room 10" in NCP:
			NCP.remove("Room 10")
	if "Room 11" in NCP:
			NCP.remove("Room 11")
	if "Room 12" in NCP:
			NCP.remove("Room 12")
	if "Room 13" in NCP:
			NCP.remove("Room 13")
	if "Room 14" in NCP:
			NCP.remove("Room 14")
#vamos ver quantas pessoas existem nos corredores e nos quartos
	for i in range(len(lista)):
		if "person_" in lista[i][0] and "Corredor 2" in lista[i][1]:
			nCP +=1
		elif "person_" in lista[i][0] and "Corredor 1" in lista[i][1]:
			nCP +=1
		elif "person_" in lista[i][0] and "Corredor 3" in lista[i][1]:
			nCP +=1
		elif "person_" in lista[i][0] and "Corredor 4" in lista[i][1]:
			nCP +=1
		
		elif "person_" in lista[i][0] and "Room 5" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 6" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 7" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 8" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 9" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 10" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 11" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 12" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 13" in lista[i][1]:
			nSP +=1
		elif "person_" in lista[i][0] and "Room 14" in lista[i][1]:
			nSP +=1

	aux=int(len(NCP))
	AUX=int(len(NSP))

    #Dependendo dos dados que temos, pode sair um resultado diferente

	if ( AUX==0 and nSP==0 and nCP==0):
		print "nao temos dados suficientes"
	elif (AUX==0 and nSP==0 and nCP!=0):
		print " É mais provavel encontrar pessoas nos corredores"
	elif ( AUX!=0 and nSP==0 and nCP==0):
		print "nao temos dados suficientes"
	elif (AUX!=0 and nSP!=0 and nCP==0):
		print " É mais provavel encontrar pessoas nos QUARTOS"
	elif (AUX!=0 and nCP!=0 and nSP==0):
		print " É mais provavel encontrar pessoas nos corredores"
	elif((float(nCP)/aux)> (float(nSP)/AUX)):	
		print " A probabilidade é maior nos CORREDORES"
	elif( (float(nCP)/aux)< (float(nSP)/AUX)):	
		print " A probabilidade é maior nos quartos"
	elif((float(nCP)/aux)== (float(nSP)/AUX)):	
		print " A probabilidade é IGUAL"

def roomTipo(x,y):
	global sala_ant,suites,single,double,meeting,generic
	
	
	bed = 0
	room = local(x,y)
    #vamos verificar se a sala onde estamos nao é uma porta e se a sala anterior nao é um corredor para ser uma suite
	if room!="Porta" and sala_ant != "Corredor 1" and sala_ant != "Corredor 2" and sala_ant != "Corredor 3" and sala_ant != "Corredor 4" and room != "Corredor 1" and room != "Corredor 2" and room != "Corredor 3" and room != "Corredor 4" and sala_ant != "Elevador 0" and sala_ant not in suites and room not in suites:
		obj_room = objectRoom(room)
		obj_room_ant = objectRoom(sala_ant)
	
    #vamos verificar se existe uma cama na sala atual ou na sala anterior para afirmarmos que é uma suite
    		for x in range(len11(obj_room)):
			if "bed" in str(obj_room[x]):
				bed += 1
		for y in range(len(obj_room_ant)):
			if "bed" in str(obj_room_ant[y]):
				bed += 1					
		if bed > 0 :
			suites.append(room)
			suites.append(sala_ant)
		
		
def objectRoom(obj_room): 

	room11 = []
	room12 = []
	room13 = []
	room14 = []
	room5 = []
	room6 = []
	room7 = []
	room8 = []
	room9 = []
	room10 = []
	room11 = []
	room =""
    #vamos juntar os objetos de cada quarto numa lista e depois é devolvida a lista de acordo com a sala obj_room
	for x in range(len(lista)):

		if lista[x][1] == "Room 11":
			room11.append(str(lista[x][0]))
		elif lista[x][1]== "Room 12":
			room12.append(str(lista[x][0]))
		elif lista[x][1]== "Room 13":
			room13.append(str(lista[x][0]))
		elif lista[x][1]== "Room 14":
			room14.append(str(lista[x][0]))
		elif lista[x][1]== "Room 5":
			room5.append(str(lista[x][0]))
		elif lista[x][1]== "Room 6":
			room6.append(str(lista[x][0]))
		elif lista[x][1]== "Room 7":
			room7.append(str(lista[x][0]))
		elif lista[x][1]== "Room 8":
			room8.append(str(lista[x][0]))
		elif lista[x][1]== "Room 9":
			room9.append(str(lista[x][0]))
		elif lista[x][1]== "Room 10":
			room10.append(str(lista[x][0]))


	if obj_room == "Room 11":
		return room11
	elif obj_room == "Room 12":
		return room12
	elif obj_room == "Room 13":
		return room13
	elif obj_room == "Room 14":
		return room14
	elif obj_room == "Room 5":
		return room5
	elif obj_room == "Room 6":
		return room6
	elif obj_room == "Room 7":
		return room7
	elif obj_room == "Room 8":
		return room8
	elif obj_room == "Room 9":
		return room9
	elif obj_room == "Room 10":
		return room10

			
def Pergunta4():
	global lista,visitadas,suites
	aux=copy.copy(visitadas)
	aux2=[]

	if "Corredor 2" in aux:
		aux.remove("Corredor 2")
	if "Corredor 1" in aux:
		aux.remove("Corredor 1")
	if "Corredor 3" in aux:
		aux.remove("Corredor 3")
	if "Corredor 4" in aux:
		aux.remove("Corredor 4")
	if int(len(aux))==0:
		print"Nao temos informção suficiente, nenhum quarto visitado ate ao momento"

	else:
		
		aux=[ i for i in aux if i not in suites]		
		
		
		for i in range(len(aux)):
			bed=0
			pc=0
			chair=0
			table=0
			obj_room=objectRoom(aux[i])
			#para se verificar o tipo de quarto e se existe algum pc 
			for x in range(len(obj_room)):	
				obj = str(obj_room[x].split("_")[0])			
				if "bed" == obj:
					bed += 1
				if "computer" == obj:
					pc += 1
				if "chair" == obj:
					chair += 1
				if "table" == obj:
					table += 1
				
			if bed==1 and pc!=0 and "single" not in aux2:
				aux2.append("single")
			elif bed==2 and pc!=0 and "double" not in aux2:
				aux2.append("double")
			elif bed==0 and chair >1 and table==1 and pc!=0 and "meeting" not in aux2:
				aux2.append("meeting")
			else:
				if "generic" not in aux2 and pc!=0:
					aux2.append("generic")
		
		for i in range(len(suites)):
			pc=0
			obj_room=objectRoom(suites[i])
			#vamos verificar se existe algum pc em alguma suite para s adicionar a lista que vai dar o print 
			for x in range(len(obj_room)):
				obj=str(obj_room[x].split("_")[0])
				if "computer" in obj:
					pc+=1

			if "suites" not in aux2 and pc!=0:
				aux2.append("suites")
		
		for i in range(len(aux2)):
				print aux2[i]


def Pergunta5():
	global suites,visitadas,lista,x_ant,y_ant
	obj_room=[]
	aux=[]
	aux2=[]
	obj=""
	obj_room=[]
	novo_min=""
	minimo=100 #definiu-se o minimo 100 no inicio pois assim como no grafo nao há mais do que 14 salas, o tamanho do caminho que a função nos vais dar vai ser sempre inferior a este valor
	aux=copy.copy(visitadas)

	if "Corredor 2" in aux:
		aux.remove("Corredor 2")
	if "Corredor 1" in aux:
		aux.remove("Corredor 1")
	if "Corredor 3" in aux:
		aux.remove("Corredor 3")
	if "Corredor 4" in aux:
		aux.remove("Corredor 4")
	if int(len(aux))==0:
		print"Nao temos informção suficiente, nenhum quarto visitado ate ao momento"

	else:
		l2=set(suites)
		aux=[ i for i in aux if i not in suites]		
		
		
		print aux
		for i in range(len(aux)):
			bed=0
			obj_room=objectRoom(aux[i])
			
			for x in range(len(obj_room)):	
				obj = str(obj_room[x].split("_")[0])			
				if "bed" == obj:
					bed += 1
				
			if bed==1:
				aux2.append(str(aux[i]))

		if int(len(aux2))==0:
			print"Ainda nao foram encontrados quartos individuais"

		else:
			print bed
			print aux2
			for x in range(len(aux2)):
				target = int(aux2[x].split(" ")[1])
				begin = int(str(local(x_ant,y_ant)).split(" ")[1])
				print begin
				path = nx.shortest_path(G,begin,target)
				if(int(len(path)) < minimo ):
					minimo = path
					novo_minimo = aux2[x]
	
			if local(x_ant,y_ant)==novo_minimo:
				print "	Ja esta num quarto individual"	
			print novo_minimo



# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')

	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()


# ---------------------------------------------------------------
if _name_ == '_main_':
	agent()
