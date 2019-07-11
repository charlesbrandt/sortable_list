# Sortable

A collection of re-usable Python (server side) and Javascript (client side) components that assist with manually sorting a group of items.

## Cool, where do I begin?

Clone this repository:

     git clone https://github.com/charlesbrandt/sortable

Then open a terminal:

    cd /path/to/local/repo/sortable/frontend/
    npm run dev

(or yarn)

## Goal

Sorting is useful in many different applications. Often considerable time goes in to recreating, re-engineering and re-implementing this task. This project aims to serve as a foundation for this style of interface when the need arises.

Arguably, the option to specify a manual order should be available for all types of collections.

## Overview

Most sorted lists can be distilled down to a textual representation where each item is on its own line in a file, and the items are sorted top to bottom. Having a textual representation is nice for manually editing the order directly in the text list. This also makes it easy to store the results of the sort operation.

The tricky part comes when it's time to associate the item string in the text list with the loaded, more robust, object representation of the item. By defining a common item object that is a super set for most common item attributes, we can normalize items across many types and show the associated meta data accordingly, when it's available.

## Requirements

This project utilizes bottle for the micro python framework.

http://bottlepy.org/docs/dev/index.html

It also utilizes the excellent javascript "Sortable" library:

https://rubaxa.github.io/Sortable/

## References

Loosely based on pose project from:

https://github.com/charlesbrandt/mindstream
