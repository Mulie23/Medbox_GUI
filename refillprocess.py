def refillProcess() : 
    # pull updated prescription 
    container = Containers(DIR, STEP, SLEEP) 
    stateMachine = True ; 
    state = 'barcode'
    while(stateMachine) : 
        if (state=="barcode") : 
            #display the relevant details on the front end - Wentao
            scan_window.show(wait=True)
            # information on what medicine are to be filled up 
            medicine_id = checkBarcode() ; 
            if medicine_id!=None : 
                state = "rotate"

            # add GUI interrupt 
        elif (state=="rotate") : 
            container_id = container.getContainer(medicine_id)
            if container.rotateContainerToRefillArea() : 
                state="wait"
            else : 
                state = "error"
                message = "couldn't rotate container"
        elif (state=="wait") : 
            scan_window.hide()
            quantity_window.show(wait=True)
            # wait for a button push on gui and number of pills form input 
            # update infromation i.e container.json
            if refillComplete() : 
                state = "finish"
            else : 
                state = "barcode" 
        elif (state=="finish"): 
            container.writeToFile() 
            stateMachine = False 
        elif  (state=="error") : 
            error = "there was some error" 
            stateMachine = False 
        else : 
            state = "error" 
            error = "invalid sate" 

    return  True     