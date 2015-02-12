from YaasController import *

looper_last_track_index = 0

class LooperController(YaasController):
    __module__ = __name__
    __doc__ = 'LooperController'
    
    emulatedLoopClip = {}
      
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(LooperController) init")    
    
    def get_looper_index_in_returns(self, targetcount):
        
        rts = self.song().return_tracks
        count = 0
        for i in range(len(rts)):

            if LOOPER in rts[i].name:
                count = count + 1
            if targetcount == count:
                return i
    
    def activate_looper(self, param, value):
        
        index = param[0]
        selected_track = self._parent._song_helper.get_selected_track()
        looperindex = self.get_looper_index_in_returns(index)
        if selected_track.get_send_value(looperindex) == MAX_LOOPER:
            selected_track.set_send_value(looperindex, MIN_LOOPER)
        else:
            selected_track.set_send_value(looperindex, MAX_LOOPER)
        
    def switch_view(self, param, value):
        
        index = param[0]
        global looper_last_track_index
        self.log.debug("test switch_view for " + str(index))
        
        looperindex = self.get_looper_index_in_returns(index)
        
        if looper_last_track_index is None:
            # gehe zu looper
            self.log.debug("zum looper ")
            looper_last_track_index = self._parent._song_helper.get_selected_track().get_track_index() 
            self.song().view.selected_track = self.song().return_tracks[looperindex]
        else:        

            self.log.debug("zur spur " + str(looper_last_track_index))
            self.song().view.selected_track = self.song().tracks[looper_last_track_index]
            looper_last_track_index = None
            
    def clipLooper(self, params, value):
        """ 
            Records a clip in the current track.
            First press is record.
            Second is play
            0 -> track_index
        """
        self.log.verbose("(LooperController) clipLooper called")
        track_index = params[0]
        self.log.verbose("(LooperController) for track " + str(track_index))

        track_helper = self.track_helper(track_index)
        if track_helper.get_track().arm == False:
            track_helper.arm()
        track_helper.get_track_index()
        self.log.verbose("(LooperController) 1 ")
        
        current_slot = None;
        self.log.verbose("(LooperController) 2 ")
        if str(track_index) in self.emulatedLoopClip:
            current_slot = self.emulatedLoopClip[str(track_index)]
        self.log.verbose("(LooperController) 3 ")
        self.log.debug("Emulate Looper 2 for track " + str(track_index) + " with slot " + str(current_slot))
        
        track = self.song().tracks[track_index]
        i = 0
        foundClip = None
        while i<50:            
            if i>=len(track.clip_slots):
                self.log.debug("did not find empty clip until " + str(i))
                break;
            clip = track.clip_slots[i].clip

            if clip == None and (len(track.clip_slots) > i+1 and track.clip_slots[i+1].clip == None) and (len(track.clip_slots) > i+2 and track.clip_slots[i+2].clip == None): 
                self.log.debug("Clip " + str(i+1) + " is empty");
                foundClip = i
                i = 50;
            i = i + 1

        if foundClip != None:
            if current_slot != None:
                
                if track.clip_slots[current_slot].is_recording:
                    
                    track.clip_slots[current_slot].stop()
                    track.clip_slots[current_slot].fire()
                    del self.emulatedLoopClip[str(track_index)]
                else:
                    self.log.debug("else")
                    i = current_slot
                    while i<50:            
                        clip = track.clip_slots[i].clip
                        #self.log.debug("Clip " + str(clip));
                        if clip == None:
                            #self.log.debug("Clip " + str(i) + " is empty");
                            foundClip = i
                            i = 50;
                        i = i + 1
                    track.clip_slots[foundClip].fire()
                    self.emulatedLoopClip[str(track_index)] = foundClip
            else:
                self.log.debug("Switch Looper 1")
                track.clip_slots[foundClip].fire()
                self.emulatedLoopClip[str(track_index)] = foundClip

        