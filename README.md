# FOIAbility Workshop Technical Notes

## Set up your virtual machine

Using Oracle's VirtualBox

### Networking

NAT with port forwarding. Ports to forward:

1.	ssh (anything but 22 on host)
1.	Solr (defaults to 8983)

### Check access via SSH

## Installing dependencies

### Install git

The resources and examples for this workshop are on Github. In order to use github on your virtual machine, you're going to need to set up git.

```
sudo apt-get install git
```

### Grab this repository and its submodules

```
git clone https://github.com/harlo/FOIAbility-Workshop.git
cd FOIAbility-Workshop
git submodule update --init --recursive

```

### Install some Linux packages

Here's a handy script to set up your virtual machine with everything else it needs.

```
#!/bin/bash

# download dependencies
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install zip unzip python-dev python-pip build-essential make gcc oracle-java8-installer

# set java path properly
echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> ~/.bash_aliases
echo "PATH=$PATH:$JAVA_HOME/bin" >> ~/.bash_aliases
source ~/.bashrc
```

### Python packages

All of the python modules you'll need are listed in `requirements.txt`. To install them, simply run `sudo pip install -r requirements.txt` and follow any prompts.

## Installing the Stanford NER package

The Stanford Named Entity Recognizer package allows you to find people, places, businesses, organizations, and more in a given text. These are called entities.

### 1. Download and unpack

```
wget -O stanford-ner.zip http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip
unzip stanford-ner.zip
```

### 2. Install PyNER

PyNER is a python package that provides easy interface with the NER software you downloaded. It's already included as a submodule in this project, but you have to manually install and set it up.

```
cd ~/FOIAbility-Workshop/lib/PyNER
sudo python setup.py install
```

### 3. Test it out

Before we start scripting the NER, let's just test it for basic functionality:

```
echo "I complained to Microsoft about Bill Gates" >> ~/test_NER.txt
cd stanford-ner-2015-12-09
java -mx600m -cp "*:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -outputFormat inlineXML -textFile ~/test_NER.txt
rm ~/test_NER.txt
```

If all goes well, this should output something like:

```
I complained to <ORGANIZATION>Microsoft</ORGANIZATION> about <PERSON>Bill Gates</PERSON>
CRFClassifier tagged 15 words in 1 documents at 137.61 words per second.
```

Going forward, we're going to be batch processing text using the NER, so it will need to function as a server running on port 2020. Create an alias to make that easy for you by appending the following to your `~/.bash_aliases` file:

```
alias NER='cd ~/stanford-ner-2015-12-09 && java -mx600m -cp "*:lib/*" edu.stanford.nlp.ie.NERServer -port 2020 -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -outputFormat inlineXML &'
```

## Installing Apache Solr

### 1. Download and import Apache developers' signing keys

```
wget -O solr_keys.asc https://archive.apache.org/dist/lucene/solr/6.3.0/KEYS
gpg --import solr_keys.asc
```

### 2. Download the software package and corresponding signature file

```
wget https://archive.apache.org/dist/lucene/solr/6.3.0/solr-6.3.0.tgz
wget https://archive.apache.org/dist/lucene/solr/6.3.0/solr-6.3.0.tgz.asc
```

### 3. Verify the download against the PGP data

```
gpg --verify solr-6.3.0.tgz.asc solr-6.3.0.tgz
```

### 4. Unpack and set it up

IF VERIFICATION succeeds, proceed to unpack Solr to homedir, and alias it as `solr` to make it easier to run commands.

```
tar -xvzf solr-6.3.0.tgz
echo "alias solr=~/solr-6.3.0/bin/solr" >> ~/.bash_aliases
source ~/.bashrc
```

### 5. Check to see if Solr works

Try starting it in the foreground with `solr start -f`, and navigate to `http://localhost:8983` to view the details of the instance. When you're done, you can simply press `CTRL-c` to stop it.

### 6. Create your core.

In Solr-speak, a *core* is a collection that is capable of indexing and searching through any documents pushed to it.
