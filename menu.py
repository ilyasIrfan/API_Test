import uvicorn
import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

with open("menu.json","r") as read_file:
	data = json.load(read_file)
app = FastAPI()

@app.get("/")
def root():
	return{'Menu','Item'}

@app.get("/menu")
async def read_menus():
	return data

@app.get("/menu/{item_id}")
async def read_menu(item_id : int):
	for menu_item in data['menu']:
		if menu_item['id'] == item_id:
			return menu_item
	raise HTTPException(
			status_code = 404,
			detail = f'Item not found'
		)

@app.post('/menu')
async def add_menu(name : str):
	id = 1
	if(len(data['menu']) > 0): #buat base id
		id = data['menu'][len(data['menu']) - 1]['id']+1 #cari record terakhir dan akses id
	n_data = {'id': id,'name' : name}
	data['menu'].append(dict(n_data))
	read_file.close()
	with open("menu.json","w") as write_file:
		json.dump(data,write_file,indent = 4) #agar rapi indent = 4
	write.file.close()
		
	return n_data
	# raise HTTPException(
	# 		status_code = 500,
	# 		detail = f'Internal server error'
	# 	)

@app.put("/menu/{item_id}")
async def update_menu(item_id : int, name : str):
	for menu_item in data['menu']:
		if menu_item['id'] == item_id:
			menu_item['name'] = name
			read_file.close()
			with open("menu.json","w") as write_file:
				json.dump(data,write_file,indent = 4) #agar rapi indent = 4
			write.file.close()

			return("message : data updated successfully!!")

	raise HTTPException(
			status_code = 404,
			detail = f'Item not found'
		)


@app.delete("/menu/{item_id}")
async def delete_menu(item_id : int):
	for menu_item in data['menu']:
		if menu_item['id'] == item_id:
			data['menu'].remove(menu_item)
			read_file.close()
			with open("menu.json","w") as write_file:
				json.dump(data,write_file,indent = 4) #agar rapi indent = 4
			write.file.close()

			return("message : data deleted successfully!!")

	raise HTTPException(
			status_code = 404,
			detail = f'Item not found'
		)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
