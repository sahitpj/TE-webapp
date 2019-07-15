cd ..

echo "Make sure you have python3 installed"

echo "Installing python dependencies"

pip3 install -r requirements.txt

python3 -m spacy download en

echo "make sure you have java8 installed"

wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip

unzip stanford-corenlp-full-2018-10-05.zip

cd stanford-corenlp-full-2018-10-05

echo "-----------------------"
echo "Starting coreNLP server"
echo "-----------------------"

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000