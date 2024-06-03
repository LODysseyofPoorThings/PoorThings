<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="1.0">

<xsl:output method="html" indent="yes"/>
    
    <!-- Match TEI elements and transform them to HTML -->
    <xsl:template match="/">
        <html>
            <head>
                <title>
                    <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                </title>
                <style>
                        body {
                            font-family: 'Montserrat', Arial, sans-serif;
                            margin: 20px;
                            background-color: #ffe4e1; 
                        }
                    
                        .metadata {
                            padding-bottom: 10px;
                            margin-bottom: 20px;
                        }
                        .right-indent {
                            margin-left: 20em;
                        }
                    </style>
            </head>
            <body>
                <div class = "metadata">
                    <h1>
                        <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']"/>
                    </h1>
                    <h2>
                        <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='sub']"/>
                    </h2>
                    <p>
                        <b>Author: </b> <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author"/>
                    </p>
                    <p>
                        <b>Publisher: </b> <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher/tei:orgName" />
                    </p>
                    <p>
                        <b>Publication year: </b> <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:biblStruct/tei:monogr/tei:imprint/tei:date" />
                    </p>
                    <p>
                        <b>ISBN: </b> <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno[@type='ISBN']" />
                    </p>
                </div>
                <div>
                  <h3>List of Characters</h3>
                  <ul>
                    <xsl:for-each select="//tei:listPerson/tei:person/tei:persName">
                        <li>
                            <xsl:value-of select="tei:forename"/> 
                            <xsl:value-of select="tei:surname"/>
                            <xsl:if test="tei:addName">
                                (<xsl:value-of select="tei:addName"/>)
                            </xsl:if>
                        </li>
                    </xsl:for-each>
                  </ul>
                </div>
                
                <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
                
            </body>
        </html>
    </xsl:template>

    <!-- Template to match <body> -->
    <xsl:template match="tei:body">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!-- Text in italic -->
    <xsl:template match="tei:div[@type='text' and @rend='rend-it']">
        <i>
          <xsl:apply-templates/>
        </i>
    </xsl:template>
    
    <!-- Template for head element -->
    <xsl:template match="tei:head">
        <header>
            <h4>
                <xsl:apply-templates/>
            </h4>
        </header>
    </xsl:template>

    <!-- Template for opener element -->
    <xsl:template match="tei:opener">
        <div class="opener">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- Template for salute element -->
    <xsl:template match="tei:salute">
        <span class="salute">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- Template for persName element -->
    <xsl:template match="tei:persName">
        <span class="persName">
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
    <!-- Template to match <l> elements with rend="right" -->
    <xsl:template match="tei:l[@rend='right']">
        <span class="right-indent">
          <xsl:apply-templates/>
        </span>
        <br/>
    </xsl:template>
    
    <!-- Template to match <l> elements without rend="right" -->
    <xsl:template match="tei:l[not(@rend='right')]">
        <span>
          <xsl:apply-templates/>
        </span>
        <br/>
    </xsl:template>

     <!-- Template to match <q> elements rendition without quotes -->
    <xsl:template match="tei:q[@rend='noQuotes']">
        <span class="quote noquotes">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- Template to match <q> elements rendition with quotes only in the beginning -->
    <xsl:template match="tei:q[@rend='beginQ']">
        <span class="quote noquotes">
          <xsl:text>"</xsl:text>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
    <!-- Template to match <q> elements rendition with quotes only in the ending -->
    <xsl:template match="tei:q[@rend='endQ']">
        <span class="quote noquotes">
            <xsl:apply-templates/>
            <xsl:text>"</xsl:text>
        </span>
    </xsl:template>
    
    <!-- Generic template to match <q> elements -->
    <xsl:template match="tei:q">
        <span class="quote">
            &#8220;<xsl:apply-templates/>&#8221;
        </span>
    </xsl:template>
    
    <!-- Template for <p> element -->
    <xsl:template match="tei:p">
        <p>
            <xsl:apply-templates select="node()[not(self::tei:lb)]"/>
        </p>
    </xsl:template>
    
    <!-- Convert line breaks -->
    <xsl:template match="tei:lb">
        <br/>
    </xsl:template>
    
</xsl:stylesheet>