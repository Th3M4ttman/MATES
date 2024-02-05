from pokeutil import *

def test():
	expected = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: True, 8: True, 9: True, 10:True}
	expected_mons = {7:["Rapidash" for _ in range(5)], 8:["Rapidash" for _ in range(5)], 9:["Meowth"], 10:["Pidgey"]}
		
	#init_out_of_combat()
	failed = 0
	
	i = 0
	for i in range(1, 11):
		basearray = cv2.imread(f"{PATH}/tests/{i}.png")
		base = Image.fromarray(basearray)
		cropped = np.array(deepcopy(base).crop((0,0,3040,400)))
				
		in_combat = not out_of_combat(base) and count_mons(cropped) > 0
		if  in_combat != expected[i]:
			print("Case", i, "Failed")
			failed += 1
		
		if i in expected_mons.keys():
			if get_mons(basearray) != expected_mons[i]:
				print("Case", i, "Failed\nExpected: ", expected_mons[i], "\nGot: ", get_mons(basearray))
				failed += 1
				Image.fromarray(basearray).save(f"{PATH}/tests/wtf.png")
				
		
		
	
	if failed > 0:
		print("Failed", failed, "cases")
		return False
	else:
		print("Passed all cases")
		return True

if __name__ == "__main__":
	print("Running tests")
	test()