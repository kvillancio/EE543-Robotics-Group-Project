import matlab.engine
eng = matlab.engine.start_matlab()


result = eng.sqrt(4.0)
print(f"The square root of 4.0 is {result}")
eng.quit()