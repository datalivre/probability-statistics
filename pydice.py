# _*_ coding:utf-8 _*_

# PyDice
# @author Robert Carlos                                 #
# email robert.carlos@linuxmail.org                     #
# 2018-08-07 (CC BY 3.0 BR)                             #

from statistics import mean, median, stdev
import datetime
import random

from pygal.style import Style
from pygal import Bar


custom_style = Style(
    colors=('#4747d1',),
    background='white'
)


class PyDice():
    '''Simula o lançamento de n dados'''

    def __init__(self, sides, dice, shooter):
        self.sides = sides
        self.dice = dice
        self.shooter = shooter
        self.results = []
        self.frequencies = []
        self.max_results = self.sides * self.dice

    def come_out_roll(self):
        '''
        Este método utiliza o atributo shooter para 
        decidir quantas vezes irá lançar os dados, o laço for, 
        por sua vez, simula a quantidade de dados da mão do jogador. 
        Os resultados são somados ainda dentro do laço for e 
        só então  armazenados em results.
        '''
        shoot = self.shooter
        add_up = 0
        while shoot > 0:
            random.seed(datetime.datetime.now())
            for d in range(self.dice):
                add_up += random.randint(1, self.sides)

            self.results.append(add_up)
            add_up = 0
            shoot -= 1

        return self.results

    def dice_freq(self):
        '''
        Retornar a frequência que cada número ocorre na lista Result[]
        para a geração do gráfico de frequência. O resultado é armazenado 
        na lista frequencies que é usada  como variável de  retorno.
        '''
        for d in range(self.dice, self.max_results + 1):
            self.frequencies.append(self.results.count(d))

        return self.frequencies


class DiceGraph(PyDice):
    '''
    Utiliza a classe Pygal e PyDicepara gerar gráfico 
    baseado na frequência dos dados.
    '''

    def __init__(self, sides=6, dice=2, shooter=360):
        super().__init__(sides, dice, shooter)
        self.come_out_roll = self.come_out_roll()
        self.dice_freq = self.dice_freq()
        self.chart = Bar(print_values=True,
                         print_values_position='top',
                         print_zeroes=False,
                         style=custom_style)

    def dice_graphics(self):
        '''
        Retorna um gráfico de barras contído de média, mediana e
        desvio padrão.
        '''
        dice_mean = round(mean(self.dice_freq), 2)
        dice_median = round(median(self.dice_freq), 2)
        dice_desvpa = round(stdev(self.dice_freq), 2)

        self.chart.title = "Resultado obtido ao jogar " + str(self.dice) + \
            " dado(s) D" + str(self.sides) + " " + \
            str(self.shooter) + " vez(es)."

        self.chart.x_labels = list(range(self.dice, self.max_results+1))
        self.chart.x_title = "Resultado\n" + "Média " + str(dice_mean) + "," \
            " Mediana " + str(dice_median) + "," \
            " Desvio padrão " + str(dice_desvpa) + "."

        self.chart.y_title = 'Frequência'
        self.chart.add('Dados', self.dice_freq)
        self.chart.render_to_file('rcg_chart_resultado.svg')

    def terminal(self):
        '''Classe que exibe os resultados em texto.'''
        print('Dados sorteados:      ' + str(self.come_out_roll[:11]))
        print('Frequência dos dados: ' + str(self.dice_freq))


def dice_gen():
    lados = 6
    dados = 2
    rodada = 360

    dice = DiceGraph(sides=lados, dice=dados, shooter=rodada)
    dice.dice_graphics()
    dice.terminal()


dice_gen()
