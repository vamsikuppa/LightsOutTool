from my_app import app, login_manager, db
from flask import g, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from my_app.product.models import User, LoginForm, RegistrationForm, envLabels
from paramiko import client
import re
import json
from werkzeug import abort


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def get_current_user():
    g.user = current_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('This username is already taken', 'warning')
            return render_template('register.html', form=form)
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered kindly signin', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        registereduser = User.query.filter_by(username=username).first()
        if not (registereduser and registereduser.check_password(password)):
            flash('Username or password is not valid', 'error')
            return render_template('login.html', form=form)
        login_user(registereduser)
        flash('Logged in successfully', 'success')
        return redirect(url_for('trigger'))
    return render_template('login.html', form=form)


@app.route('/trigger')
def trigger():
    envlabels = envLabels.query.all()  # Getting Env labels
    resEnvLabels = {}
    for envlabel in envlabels:
        resEnvLabels[envlabel.id] = {
            'envLabel': envlabel.envLabel,
            'envName': envlabel.envName,
            'orderProp': envlabel.orderProp,
            'provFile': envlabel.provFile
        }
    global Client
    Client = connect_ssh("slc10xkv.us.oracle.com", "atangudu", "1989@nudeeP")
    if not Client:
        abort(500)  # Internal Server Error
    command = "ade showlabels -series FAINTEG_MAIN_PLATFORMS | tail -10"
    fainteglabels = []
    stdin, stdout, stderr = Client.exec_command(command)
    while not stdout.channel.exit_status_ready():
        # Print data when available
        if stdout.channel.recv_ready():
            alldata = stdout.channel.recv(1024)
            prevdata = b"1"
            while prevdata:
                prevdata = stdout.channel.recv(1024)
                alldata += prevdata
            commandOutput = (str(alldata.encode("utf8")).split('\n'))
    fainteglabels = filter(None, commandOutput)
    return render_template('trigger.html', envlabels=resEnvLabels, fainteglabels=fainteglabels)


@app.route('/get_faat_labels/')
def get_faat_labels():
    runName = request.args.get('runName').encode('utf-8')
    fincExp = re.compile(r'FINC')  # Exp for FINC
    findExp = re.compile(r'FIND')  # Exp for FIND
    if fincExp.search(str(runName)):
        command = "ade showlabels -series FAAT_PT.V2MIBFINC_GENERIC | tail -10"
        commandOutput = []
        stdin, stdout, stderr = Client.exec_command(command)
        while not stdout.channel.exit_status_ready():
            # Print data when available
            if stdout.channel.recv_ready():
                alldata = stdout.channel.recv(1024)
                prevdata = b"1"
                while prevdata:
                    prevdata = stdout.channel.recv(1024)
                    alldata += prevdata
                commandOutput = (str(alldata.encode("utf8")).split('\n'))
        commandOutput = filter(None, commandOutput)
    else:
        command = "ade showlabels -series FAAT_PT.V2MIBFIND_GENERIC | tail -10"
        commandOutput = []
        stdin, stdout, stderr = Client.exec_command(command)
        while not stdout.channel.exit_status_ready():
            # Print data when available
            if stdout.channel.recv_ready():
                alldata = stdout.channel.recv(1024)
                prevdata = b"1"
                while prevdata:
                    prevdata = stdout.channel.recv(1024)
                    alldata += prevdata
                commandOutput = (str(alldata.encode("utf8")).split('\n'))
        commandOutput = filter(None, commandOutput)  # To remove empty values
    jsondata = json.dumps(commandOutput, indent=4, ensure_ascii=False)
    return jsondata

@app.route('/trigger/output', methods=['POST'])
def output():
    selectOption = request.form.get('runName')
    faatLabel = request.form.get('faatlabel')
    faintteg=request.form.get('faintteg')
    query_string = "SELECT orderProp,provFile FROM env_labels WHERE envName='{}'".format(selectOption.encode('utf-8'))
    result = db.engine.execute(query_string)
    envResult = result.fetchall()
    for row in envResult:
        envOrderProp = row[0].encode('utf-8')
        envProvFile = row[1].encode('utf-8')
    command = "/usr/local/packages/aime/dte/DTE3/bin/jobReqAgent -topoid 93289 -s /tmp -p LINUX.X64 -l " \
              "{} -report -e anudeep.tangudu@oracle.com,sandeep.s.srivastava@oracle.com -a /usr/local/packages/aime/dte/DTE -w " \
              "/scratch/atangudu/AUTO_WORK/job2 -topoalias=""R13_Auto_Sandbox_Run"" " \
              "PILLAR_TYPE=FSCM RunFaBATS:CMDOPTIONS='-parallel IS_ALM=true FA_TEMPLATE=%FA_TEMPLATE% " \
              "FAAT_LABEL={} " \
              "ORDER_INPUTFILE={}' " \
              "PROVISIONING_PLAN={} REE_PARAM=""OSPlayabackBrowser=Firefox""".format(faintteg,faatLabel, envOrderProp,
                                                                                     envProvFile)
    stdin, stdout, stderr = Client.exec_command(command)
    while not stdout.channel.exit_status_ready():
        # Print data when available
        if stdout.channel.recv_ready():
            alldata = stdout.channel.recv(1024)
            prevdata = b"1"
            while prevdata:
                prevdata = stdout.channel.recv(1024)
                alldata += prevdata
            commandOutput = (str(alldata.encode("utf8")))
    dteId = refactor_commandOutput(commandOutput)
    return render_template("output.html", commandOutput=dteId)

def refactor_commandOutput(commandOutput):
    dteidMatch = re.search(r'\d{8} : SMC_LIGHTS_OUT_BATS', commandOutput, re.MULTILINE)  # PERL compatible
    dteId = re.search(r'\d{8}', dteidMatch.group(0))
    return dteId.group(0)


def connect_ssh(hostname, username, password):  # store credentials it in db
    Client = client.SSHClient()
    Client.set_missing_host_key_policy(client.AutoAddPolicy())
    Client.connect(hostname=hostname, username=username, password=password)
    if not Client:
        abort(404)
    return Client


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
