import pandas as pd
from typing import *
import tabulate
from classes import SLR_Table


def SLR_simulate(content: str, reader: 'SLR_Table'):
    contentTokens: List[str] = []
    print('Content:', content)
    for element in content.split(' '):
        el = element.strip()
        if el == '':
            continue
        tk = reader.obtainGrammarElement(el)
        if tk == 1:
            raise Exception('Token not found in', element)
        if tk == 2:
            continue
        contentTokens.append(el)

    contentTokens.append('$')

    stateStack: List[int] = [reader.firstState]
    df_stack = {}
    actionsStack = []

    while True:
        for act in actionsStack:
            print(act[0])
        print('-------------------')
        stateOn = stateStack[-1]
        actualToken = contentTokens[0]
        action, desc = reader.obtainAction(stateOn, actualToken)
        stateToPrint = [st for st in stateStack]
        stateToPrint.reverse()
        df_stack['State'] = stateToPrint
        df_stack['Input'] = [tk for tk in contentTokens]
        df_stack['Action'] = [desc if not pd.isna(desc) else 'Error!']
        print(tabulate.tabulate(df_stack, headers='keys', tablefmt='psql'))

        if pd.isna(action) or action is None:
            d = reader.tablePrint.loc[stateOn].notna()
            k = reader.tablePrint.columns[d].tolist()
            print('\033[91m', 'Reject!', '\033[0m')
            print()
            print('\033[96m', "Expected...", '\033[0m')
            for exp in k:
                if exp.islower():
                    continue
                print('\033[93m', exp, '\033[0m')
            print()
            print('\033[96m', "Received...", '\033[0m')
            print('\033[93m', actualToken, '\033[0m')
            raise Exception('Error!, not accepted')
        if action[0] == 'S':
            stateStack.append(action[1])
            tokenRead = contentTokens.pop(0)
            actionsStack.append((tokenRead, 'Shift'))
        elif action[0] == 'R':
            prod: Tuple[str, int] = action[1]

            for _ in range(prod[1]):
                stateStack.pop()

            stateOn = stateStack[-1]
            A = prod[0]
            newAction, desc = reader.obtainAction(stateOn, A)
            if newAction is None or pd.isna(newAction):
                raise Exception('Action not found in', stateOn, A)
            stateStack.append(newAction[1])
        elif action[0] == 'A':
            break

    print('\033[92m','Accepted!', '\033[0m')

    return True
