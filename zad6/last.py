def loadCarlierData():
	with open('carl.data.txt','r') as file:
		data = file.read()
	data0 = data.split('\n\n')

	datasets = []
	class dataset:
		pass

	for datal in data0:
		if datal[0:4] == 'data':
			datasets.append(dataset())
			datasets[-1].name = datal.split('\n')[0]
			tmp = datal.split('\n')[2:]
			r = [int(tmp[i].split(' ')[0]) for i in range(len(tmp))]
			p = [int(tmp[i].split(' ')[1]) for i in range(len(tmp))]
			q = [int(tmp[i].split(' ')[2]) for i in range(len(tmp))]
			datasets[-1].jobs = []
			for j in range(len(r)):
				datasets[-1].jobs.append(RPQ(r[j],p[j],q[j]))
		if datal[0:4] == 'carl':
			datasets[-1].sol = datal.split('\n')[1]
	return datasets

def loadWitiData():
	with open('witi.data.txt','r') as file:
		data = file.read()
	data0 = data.split('\n\n')

	datasets = []
	class dataset:
		pass

	for datal in data0:
		if datal[0:4] == 'data':
			datasets.append(dataset())
			datasets[-1].name = datal.split('\n')[0]
			tmp = datal.split('\n')[2:]
			timeout =   [int(tmp[i].split(' ')[2]) for i in range(len(tmp))]
			p = 		[int(tmp[i].split(' ')[0]) for i in range(len(tmp))]
			priority =  [int(tmp[i].split(' ')[1]) for i in range(len(tmp))]
			datasets[-1].jobs = []
			for j in range(len(p)):
				datasets[-1].jobs.append(RPQ(timeout[j],p[j],priority[j]))
		if datal[0:4] == 'opt:':
			datasets[-1].sol = datal.split('\n')[1]
	return datasets


from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from pathlib import Path

class RPQ():
	def __init__(self,r,p,q):
		self.R = r
		self.P = p
		self.Q = q

# def CpWiti(jobs,instanceName):
# 	variablesMaxValue = 0
# 	for i in range(len(jobs)):
# 		variablesMaxValue += jobs[i].P

# 	# solver = pywraplp.Solver('simple_mip_program',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING0)
# 	solver = cp_model.CpModel()
# 	# variables :
# 	alfasMatrix = {}#attention !  dictionary−not  l i s t !
# 	for i in range(len(jobs)):
# 		for j in range(len(jobs)):
# 			alfasMatrix[i,j] = solver.NewIntVar(0,1,"alfa"+str(i)+"_"+str(j))
# 	starts = []
# 	for i in range(len(jobs)):
# 		starts.append(solver.NewIntVar(0,variablesMaxValue,"starts"+str(i)))

# 	#constrsints
# 	cmax = solver.NewIntVar(0,variablesMaxValue,'cmax')
# 	for i in range(len(jobs)):
# 		solver.Add(starts[i]>=0)
# 		# solver.Add(cmax>=starts[i]+jobs[i].P)

# 	spoznienia = []
# 	tmp_spoznienia = []
# 	for i in range(len(jobs)):
# 		spoznienia.append(solver.NewIntVar(0,variablesMaxValue,'tmp_abs_val_'+str(i)))
# 		tmp_spoznienia.append(solver.NewIntVar(0,variablesMaxValue,'tmp_abs_val__'+str(i)))
# 		solver.Add(
# 			tmp_spoznienia[-1]==(starts[i]+jobs[i].P-jobs[i].R)*jobs[i].Q
# 			)
# 		solver.AddAbsEquality(spoznienia[-1],tmp_spoznienia[-1])

# 	solver.Add(cmax>=sum([
# 		(tmp_spoznienia[i]+spoznienia[i]) for i in range(len(jobs))
# 		]))
# 	# solver.Add(cmax>=sum([
# 	# 	# (starts[i]+jobs[i].P-jobs[i].R)*jobs[i].Q
# 	# 	# ((starts[i]+jobs[i].P-jobs[i].R)+solver.AddAbsEquality(-(starts[i]+jobs[i].P-jobs[i].R)))/2*jobs[i].Q
# 	# 	for i in range(len(jobs))]))

# 	for i in range(len(jobs)):
# 		for j in range(i+1,len(jobs)):
# 			solver.Add(starts[i] + jobs[i].P <= starts[j] + alfasMatrix[i,j] * variablesMaxValue)
# 			solver.Add(starts[j] + jobs[j].P <= starts[i] + alfasMatrix[j,i] * variablesMaxValue)
# 			solver.Add(alfasMatrix[i,j] + alfasMatrix[j,i] == 1)

# 	# solver
# 	solver.Minimize(cmax)

# 	model = solver
# 	solver = cp_model.CpSolver()
# 	status = solver.Solve(model)
# 	if status is not cp_model.OPTIMAL:
# 		print("Not OPTIMAL !!!")
# 		return solver.ObjectiveValue(), None
# 	pi = []
# 	for i in range(len(starts)):
# 		pi.append((i,solver.Value(starts[i])))
# 	pi.sort(key=lambda x:x[1])
# 	return solver.ObjectiveValue(), pi


def CpWiti(jobs,instanceName):
	variablesMaxValue = 0
	for i in range(len(jobs)):
		variablesMaxValue += (jobs[i].R+jobs[i].P+jobs[i].Q)

	# solver = pywraplp.Solver('simple_mip_program',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING0)
	solver = cp_model.CpModel()
	# variables :
	alfasMatrix = {}#attention !  dictionary−not  l i s t !
	for i in range(len(jobs)):
		for j in range(len(jobs)):
			alfasMatrix[i,j] = solver.NewIntVar(0,1,"alfa"+str(i)+"_"+str(j))
	starts = []
	for i in range(len(jobs)):
		starts.append(solver.NewIntVar(0,variablesMaxValue,"starts"+str(i)))

	#constrsints
	cmax = solver.NewIntVar(0,variablesMaxValue,'cmax')
	delays = []
	for i in range(len(jobs)):
		delays.append(solver.NewIntVar(0,variablesMaxValue,'delays'+str(i)))
		solver.Add(delays[-1]>=(starts[i]+jobs[i].P-jobs[i].R)*jobs[i].Q)
		# solver.Add(starts[i]>=jobs[i].R)
		# solver.Add(cmax>=starts[i]+jobs[i].P+jobs[i].Q)
	solver.Add(cmax>=sum(delays))

	for i in range(len(jobs)):
		for j in range(i+1,len(jobs)):
			solver.Add(starts[i] + jobs[i].P <= starts[j] + alfasMatrix[i,j] * variablesMaxValue)
			solver.Add(starts[j] + jobs[j].P <= starts[i] + alfasMatrix[j,i] * variablesMaxValue)
			solver.Add(alfasMatrix[i,j] + alfasMatrix[j,i] == 1)

	# solver
	solver.Minimize(cmax)

	model = solver
	solver = cp_model.CpSolver()
	status = solver.Solve(model)
	if status is not cp_model.OPTIMAL:
		print("Not OPTIMAL !!!")
	pi = []
	ds = 0
	for i in range(len(starts)):
		pi.append((i,solver.Value(starts[i])))
		# print(solver.Value(starts[i]),jobs[i].R,solver.Value(delays[i]),-(solver.Value(starts[i])+jobs[i].P-jobs[i].R)*jobs[i].Q)
	pi.sort(key=lambda x:x[1])
	# print('sum',ds)
	return solver.ObjectiveValue(), pi


def Cp(jobs,instanceName):
	variablesMaxValue = 0
	for i in range(len(jobs)):
		variablesMaxValue += (jobs[i].R+jobs[i].P+jobs[i].Q)

	# solver = pywraplp.Solver('simple_mip_program',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING0)
	solver = cp_model.CpModel()
	# variables :
	alfasMatrix = {}#attention !  dictionary−not  l i s t !
	for i in range(len(jobs)):
		for j in range(len(jobs)):
			alfasMatrix[i,j] = solver.NewIntVar(0,1,"alfa"+str(i)+"_"+str(j))
	starts = []
	for i in range(len(jobs)):
		starts.append(solver.NewIntVar(0,variablesMaxValue,"starts"+str(i)))

	#constrsints
	cmax = solver.NewIntVar(0,variablesMaxValue,'cmax')
	for i in range(len(jobs)):
		solver.Add(starts[i]>=jobs[i].R)
		solver.Add(cmax>=starts[i]+jobs[i].P+jobs[i].Q)

	for i in range(len(jobs)):
		for j in range(i+1,len(jobs)):
			solver.Add(starts[i] + jobs[i].P <= starts[j] + alfasMatrix[i,j] * variablesMaxValue)
			solver.Add(starts[j] + jobs[j].P <= starts[i] + alfasMatrix[j,i] * variablesMaxValue)
			solver.Add(alfasMatrix[i,j] + alfasMatrix[j,i] == 1)

	# solver
	solver.Minimize(cmax)

	model = solver
	solver = cp_model.CpSolver()
	status = solver.Solve(model)
	if status is not cp_model.OPTIMAL:
		print("Not OPTIMAL !!!")
	# pi = []
	# for i in range(len(starts)):
	# 	pi.append((i,starts[i].solution_value()))
	# pi.sort(key=lambda x:x[1])
	return solver.ObjectiveValue(), None # pi

def Milp(jobs,instanceName):
	variablesMaxValue = 0
	for i in range(len(jobs)):
		variablesMaxValue += (jobs[i].R+jobs[i].P+jobs[i].Q)

	solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

	# variables :
	alfasMatrix = {}#attention !  dictionary−not  l i s t !
	for i in range(len(jobs)):
		for j in range(len(jobs)):
			alfasMatrix[i,j] = solver.IntVar(0,1,"alfa"+str(i)+"_"+str(j))
	starts = []
	for i in range(len(jobs)):
		starts.append(solver.IntVar(0,variablesMaxValue,"starts"+str(i)))

	#constrsints
	cmax = solver.IntVar(0,variablesMaxValue,'cmax')
	for i in range(len(jobs)):
		solver.Add(starts[i]>=jobs[i].R)
		solver.Add(cmax>=starts[i]+jobs[i].P+jobs[i].Q)

	for i in range(len(jobs)):
		for j in range(i+1,len(jobs)):
			solver.Add(starts[i] + jobs[i].P <= starts[j] + alfasMatrix[i,j] * variablesMaxValue)
			solver.Add(starts[j] + jobs[j].P <= starts[i] + alfasMatrix[j,i] * variablesMaxValue)
			solver.Add(alfasMatrix[i,j] + alfasMatrix[j,i] == 1)

	# solver
	solver.Minimize(cmax)
	status = solver.Solve()
	if status is not pywraplp.Solver.OPTIMAL:
		print("Not OPTIMAL !!!")
	# print(instanceName, "Cmax", solver.Objective().Value())
	pi = []
	for i in range(len(starts)):
		pi.append((i,starts[i].solution_value()))
	pi.sort(key=lambda x:x[1])
	# print(pi)
	return solver.Objective().Value(), pi


# datasets = loadCarlierData()
datasets = loadWitiData()
for dataset in datasets:
	print('Running',dataset.name)
	jobs = dataset.jobs
	cmax, sol = CpWiti(jobs,dataset.name)
	print('Expected:',dataset.sol,'\tComputed:',cmax,'\tAre equal: ',int(dataset.sol)==int(cmax))
	# print([o[0] for o in sol])
	# print(sol)
	# witi=[(sol[i][1]-jobs[sol[i][0]].R)*jobs[sol[i][0]].Q for i in range(len(jobs))]
	# print(sum(witi),witi)

