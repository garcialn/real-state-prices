# Real-State-Prices

Real State Prices is a project that aims to develop a web application to **predict both rent and aquisition values for real state properties** based on the following features:

- Property type (house or apartment)
- Address
- Property footage
- Number of bedrooms
- Number of parking spaces

---

```mermaid
flowchart TD;

    subgraph WEB-SCRAPE
        crowler{{Scrapy + Playwright}}
        style crowler fill:lightblue

        source((loft.com))
        style source fill:lightpink
    end
    
    subgraph DATA
        dt-raw((Raw Data))
        style dt-raw fill:lightpink

        dt-process((Process Data))
        style dt-process fill:lightblue
        
        dt-final((Final Data))
        style dt-final fill:lightgreen
    end

    subgraph NOTEBOOK
        ipynb-elt(Extract - Load - Transform)
        style ipynb-elt fill:lightblue

        ipynb-eda(Data Analysis - Data Viz)
        style ipynb-eda fill:lightblue
        
        ipynb-mdl(Model Development and Experiments)
        style ipynb-mdl fill:lightblue
    end

    subgraph SOURCE-CODE
        src-process{{Data Processing}}
        style src-process fill:lightblue
        
        src-mdl{{Model Creation}}
        style src-mdl fill:lightgreen
    end

    subgraph CONFIG
        subgraph MODEL
            config-lgbm[LightGBM Configuration]
            style config-lgbm fill:lightgreen

            config-xgb[XGBoost Configuration]
            style config-xgb fill:lightgreen
        end

        config-main[main]
        style config-main fill:lightblue

        config-processing[processing]
        style config-processing fill:lightblue
    end

    subgraph TESTS
        test-process{{Processing Tests}}
        style test-process fill:lightpink
    
        test-mdl{{Model Tests}}
        style test-mdl fill:lightpink
    end  

    subgraph APP
        app-deploy{{BentoML}}
        style app-deploy fill:lightgreen
    
        app-interface([Streamlit])
        style app-interface fill:lightgreen

        app-host((Deta))
        style app-host fill:lightgreen
    end    

    subgraph AUTOMATION
        auto-test{{Github Actions}}
        style auto-test fill:lightgreen
        
        auto-pipeline((Prefect))
        style auto-pipeline fill:lightgreen
    end    

    source-->crowler
    SOURCE-CODE---APP
    TESTS---APP

    ipynb-elt---ipynb-eda---ipynb-mdl

    app-deploy---app-interface-->app-host
    dt-raw-->dt-process-->dt-final   
    WEB-SCRAPE-->DATA   
    DATA-->NOTEBOOK

    config-lgbm---config-xgb
    
    src-process-->src-mdl
    
    config-main---config-processing
    config-main---MODEL

    DATA-->CONFIG
    CONFIG-->SOURCE-CODE
    SOURCE-CODE-->TESTS
    
    AUTOMATION-->SOURCE-CODE
    AUTOMATION-->APP

    test-process---test-mdl
    AUTOMATION-->TESTS
```
