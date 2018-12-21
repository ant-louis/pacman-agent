from os import system

w_list = [1, 3, 5]
p_list = [0, 0.2, 0.5, 0.7, 1]

for w in w_list:
    for p in p_list:
        system("python run.py --layout observer --bsagentfile beliefstateagent.py --agentfile randomagent.py --silentdisplay --ghostagent rightrandy --w {}  --p {} --hiddenghost".format(w,p))


