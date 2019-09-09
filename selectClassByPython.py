from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

# 2019.09.09
# lijunjie  Renmin University of China

# @description my school courses selection system is always crowded. 
# What's more, the courses I needed always show up abruptly 
# and disappear quickly( be selected by other students who 
# see them ahead of me). Thus I write this easy automated 
# courses selection tool

# #配置 driver
def driverPreparation():
	option = webdriver.ChromeOptions() # option配置
	# option.add_argument('headless') # 静默模式
	option.add_argument('–no-sandbox') # 最高权限执行
	driver = webdriver.Chrome("chromedriver.exe", options=option)
	driver.maximize_window()
	driver.implicitly_wait(20) # 隐性等待
	return driver
def findLesson():
	driver = driverPreparation()
	driver.get("https://v.ruc.edu.cn/account/login")
	driver.switch_to.frame('login-iframe')
	actions = ActionChains(driver)
	inputdiv = driver.find_element_by_xpath('//*[@id="username"]')
	actions.move_to_element(inputdiv)
	actions.click(inputdiv)
	actions.perform()
	login_window = driver.current_window_handle
	driver.find_element_by_xpath('//*[@id="username"]/input').send_keys("yourStudentId")
	driver.find_element_by_xpath('//*[@id="password"]/input').send_keys("youPassward")
	driver.find_element_by_xpath('//*[@id="login-submit"]').click()
	driver.find_element_by_xpath('//*[@id="meContainer"]/div[1]/div[3]/div[1]/div[2]/ul/li[4]/div/a').click()
	handles = driver.window_handles
	for handle in handles:
		if login_window != handle:
			driver.switch_to.window(handle)
	driver.find_element_by_xpath('//*[@id="tb"]/tbody/tr[6]/td[1]/a').click()
	driver.find_element_by_xpath('//*[@id="tb"]/tbody/tr[3]/td/a').click()
	driver.find_element_by_xpath('//*[@id="tb"]/tbody/tr[5]/td/a').click()		
	sel = driver.find_element_by_xpath('//*[@id="pageSize"]')
	Select(sel).select_by_value('100')
	select_url = driver.current_url+'?method=listJxbxx&isNeedInitSQL=true&kkyx=100400'
	# js=('var courses = document.querySelectorAll("#tb > tbody > tr:nth-child(n+3) > td:nth-child(5) > a");'
	# +'var credit = document.querySelectorAll("#tb > tbody > tr:nth-child(n+3) > td:nth-child(7) > a");'
	# +'for(var i = 0; i < courses.length; i++ ) {'
	# +	'console.log(courses[i]);'
	# +	'if(courses[i].innerHTML=="国际金融"&credit[i]=="3"){'
	# +		'document.querySelector("#tb > tbody > tr:nth-child(i+3) > td:nth-child(1) > a").click();'
	# +		'document.querySelector("#EAPForm > table:nth-child(18) > tbody > tr:nth-child(1) > td:nth-child(3) > table > tbody > tr > td.imagebut > a").click();'
	# +		'}'
	# +	'}')
	
	findIt = False
	while not findIt:
		findIt = refind(driver, findIt, select_url)
		driver.get(select_url)
		sel = driver.find_element_by_xpath('//*[@id="pageSize"]')
		Select(sel).select_by_value('100')
	driver.quit()
	
def refind(driver, findIt, select_url):
	courses = driver.execute_script('var hh = []; var text = document.querySelectorAll("#tb > tbody > tr:nth-child(n+3) > td:nth-child(5) > a");text.forEach(te=>{hh.push(te.innerHTML)});return hh;')
	courses=[cour.replace("\n","").replace("\t","").replace("  ","") for cour in courses]
	credit = driver.execute_script( 'var hh = []; var text = document.querySelectorAll("#tb > tbody > tr:nth-child(n+3) > td:nth-child(7)");text.forEach(te=>{hh.push(te.innerHTML)});return hh;')
	credit=[cred.replace("\n","").replace("\t","").replace("  ","") for cred in credit]
	for i in range(0,len(credit)):
		if courses[i]=="财政学" and credit[i]=="3" :
			driver.execute_script('document.querySelector("#tb > tbody > tr:nth-child('+str(i+3)+') > td:nth-child(1) > input").click()')
			# ; document.querySelector("#EAPForm > table:nth-child(18) > tbody > tr:nth-child(1) > td:nth-child(3) > table > tbody > tr > td.imagebut > a").click();
			driver.find_element_by_link_text('选 课(F2)').click()
			driver.switch_to.alert.accept()
			try:
				sm = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td/table').get_attribute("innerHTML")
				soup = BeautifulSoup(sm, 'html.parser')
				sm = soup.get_text()
				if "成功" in sm:
					findIt = True
					break
				else:
					driver.get(select_url)
					sel = driver.find_element_by_xpath('//*[@id="pageSize"]')
					Select(sel).select_by_value('100')
			except:
				pass			
	return findIt



if __name__ == '__main__':
	findLesson()

