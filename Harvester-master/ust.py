#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import seaborn as sns
import time

class universe_sentence_model():
    '''
    This class define the universal sentence model

    Attributes:
        minimum:        Minimum probability that the sentence will be classified to the class
        embed_labels:   ***
        g:              ***
        text_input:     ***
        embed:          ***
        embedded_text:  ***
        init_op:        ***
        session:        ***
    '''
    def __init__(self):
        self.minimum = 0.3
        self.embed_labels = {}
        self.g = tf.Graph()
        with self.g.as_default():
            self.text_input = tf.placeholder(dtype=tf.string, shape=[None])
            self.embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
            self.embedded_text = self.embed(self.text_input)
            self.init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
        self.g.finalize()
        self.session = tf.Session(graph=self.g)
        self.session.run(self.init_op)

    def embedding_text(self, text):
        result = self.session.run(self.embedded_text, feed_dict={self.text_input: [text]})
        return result
 
    def definition(self):
        '''
        The definition method initialize the embed_labes dictionary with the meaning of greed and sloth
        '''
        greed = ["excessive desire to acquire or possess more than one needs or deserves","reprehensible acquisitiveness; insatiable desire for wealth"]
        sloth = ["a disinclination to work or exert yourself","apathy and inactivity in the practice of virtue"]
        temp = {}
        temp["greed"] = []
        temp["sloth"] = []

        for des in greed:
            temp_np = self.embedding_text(des)
            temp["greed"].append(temp_np)
        temp["greed"].append(self.embedding_text("greed"))

        for des2 in sloth:
            temp_np = self.embedding_text(des2)
            temp["sloth"].append(temp_np)
        temp["sloth"].append(self.embedding_text("sloth"))

        self.embed_labels = temp


    def return_label(self, text):
        '''
        This method return the class according to the text
        Args:
            text:       Text needed to be classified
        Return:
            The class got from the model: greed, sloth, unkown(unknown)
        '''
        greed_grades = []
        sloth_grades = []
        embed_text = self.embedding_text(text)
        for meaning in self.embed_labels["greed"]:
            temp_grade = np.inner(embed_text,meaning)
            greed_grades.append(temp_grade)

        for meaning2 in self.embed_labels["sloth"]:
            temp_grade2 = np.inner(embed_text,meaning2)
            sloth_grades.append(temp_grade2)

        max_greed = max(greed_grades)
        max_sloth = max(sloth_grades)
        if((max_greed < self.minimum) and (max_sloth < self.minimum)):
            return "unkown"
        elif((max_greed > max_sloth) and (max_greed >= self.minimum)):
            return "greed"
        elif((max_sloth > max_greed) and (max_sloth >= self.minimum)):
            return "sloth"
        else:
            return "unkown"

# Singleton of the model
usm = universe_sentence_model()

# Test method
def main():
    #initialize the model with two lines
    usm.definition()
    
    t1 = time.time()
    text = "Happy New Year!"
    label = usm.return_label(text)
    print(text + ' ' + label)
    t2 = time.time()

if __name__== "__main__":
    main()
