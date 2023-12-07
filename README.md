# Solar Panel Shadow Detection Project

## Overview

The aim of this project is to develop a system for the detection of shadows and hotspots on solar panels using computer vision algorithms. The system processes images acquired by a fixed camera during the day, leveraging tools such as pvlib to understand the characteristic curves of panels in real-time conditions. The ultimate goal is to maximize energy production.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)

## Introduction

Solar energy production is influenced by various factors, including shadows or hotspots on solar panels. This project focuses on developing a solution to automatically detect and analyze these shadows from images acquired by a fixed camera throughout the day or possible hotspot present on solar panels. By employing computer vision algorithms and utilizing the pvlib library, we aim to gain insights into the characteristics of the solar panels under different lighting conditions, or in case of hotspot send an alert to manege the problem.

## Features

- **Shadow Detection**: The system employs computer vision algorithms to identify shadows or hotspots on solar panels.
- **Image Processing**: Images acquired by the fixed camera are processed to extract relevant information about the condition of the panels.
- **Data Analysis with pvlib**: Utilizing the pvlib library to analyze the characteristics of solar panels and optimize energy production.
- **Daytime Operation**: The system is designed to operate during the day, capturing images and providing real-time insights.
