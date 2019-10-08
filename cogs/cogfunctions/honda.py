import discord
import random
from pathlib import Path

path = Path('res')


# win and lose corresponds to 'you win' or 'you lose'
async def janken_process(ctx, choice):
	m = '```＼ #本田とじゃんけん ／\n@pepsi_jpn をフォローして\n本田圭佑 とじゃんけん勝負✌\n'
	m += '本田に勝てば、その場で\n#ペプシ \#ジャパンコーラ\nコンビニ無料引換えクーポンがもらえる！計16万名様！\n'
	m += 'あなたは何を出す？\n【4/19まで #毎日挑戦  #毎日11時スタート！ 】\nhttp://bit.ly/2IcJudY\n\n```'
	await ctx.send(m)

	win_rock = discord.File(path /'win_rock.mp4', filename='result.mp4')
	win_paper = discord.File(path / 'win_paper.mp4', filename='result.mp4')
	win_scissors = discord.File(path / 'win_scissors.mp4', filename='result.mp4')

	lose_rock = discord.File(path / 'lose_rock.mp4', filename='result.mp4')
	lose_paper = discord.File(path / 'lose_paper.mp4', filename='result.mp4')
	lose_scissors = discord.File(path / 'lose_scissors.mp4', filename='result.mp4')

	if choice == 'rock': # if rock, you win when honda is scissors, you lose when honda is paper
		choices = (win_scissors, lose_paper)
	elif choice == 'paper': # if paper, you win when honda is rock, you lose when honda is scissors
		choices = (win_rock, lose_scissors)
	elif choice == 'scissors': # if scissors, you win when honda is paper, you lose when honda is rock
		choices = (win_paper, lose_rock)
	
	await ctx.send(file=random.choice(choices))


async def card_process(ctx, choice):
	# win and lose corresponds to 'you win' or 'you lose'
	m = f'```＼ #本田とカードバトル ／#私は本田の{choice}を引く\n'
	m += '@pepsi_jpn をフォローして 1日1回、本田圭佑 とカードバトル！\n'
	m += '勝てば、 #ペプシ #ジャパンコーラ １ケース当たる！計1000名様！\n'
	m += '【7/22まで #毎日挑戦 #毎日11時start 】 bit.ly/2XC2lDi```'
	await ctx.send(m)

	temp = random.choice([
		'lose_cards.mp4',
		'lose_cards1.mp4',
		'lose_cards2.mp4',
		'lose_cards3.mp4',
		'win_cards.mp4'
	])
	result = discord.File(path / temp, filename='result.mp4')
	await ctx.send(file=result)