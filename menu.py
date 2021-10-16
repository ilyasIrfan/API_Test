import uvicorn
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel

with open("menu.json","r") as read_file:
	data = json.load(read_file)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="wpo9nine@gmail.com", full_name="Ilyas Irfan"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/")
def root():
	return{'Menu','Item'}

@app.get("/menu")
async def read_menus(token: str = Depends(oauth2_scheme)):
	return {"token" : token}
	# return data

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
