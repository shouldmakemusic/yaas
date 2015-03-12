"""
# Copyright (C) 2015 Manuel Hirschauer (manuel@hirschauer.net)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Manuel Hirschauer <manuel@hirschauer.net> 
"""
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
        track_helper.get_track().arm = True
        track_helper.get_track_index()
        
        saved_slot = None;
        
        if str(track_index) in self.emulatedLoopClip:
            saved_slot = self.emulatedLoopClip[str(track_index)]
        
        self.log.debug("Click Looper for track " + str(track_index) + " with slot " + str(saved_slot))
        
        track = self.song().tracks[track_index]
        i = 0
        found_empty_clip = None
        while i<50:            
            if i>=len(track.clip_slots):
                self.log.debug("did not find empty clip until " + str(i))
                break;
            clip = track.clip_slots[i].clip

            if clip == None and (len(track.clip_slots) > i+1 and track.clip_slots[i+1].clip == None) and (len(track.clip_slots) > i+2 and track.clip_slots[i+2].clip == None): 
                self.log.verbose("Clip " + str(i+1) + " is empty");
                found_empty_clip = i
                i = 50;
            i = i + 1

        if found_empty_clip != None:
            if saved_slot != None:
                
                if track.clip_slots[saved_slot].is_recording:
                    
                    # if its recording set it to play
                    track.clip_slots[saved_slot].stop()
                    track.clip_slots[saved_slot].fire()
                    del self.emulatedLoopClip[str(track_index)]
                else:
                    self.verbose('current slot is not recording')
                    # record
                    i = saved_slot
                    while i<50:            
                        clip = track.clip_slots[i].clip
                        #self.log.debug("Clip " + str(clip));
                        if clip == None:
                            #self.log.debug("Clip " + str(i) + " is empty");
                            found_empty_clip = i
                            i = 50;
                        i = i + 1
                    track.clip_slots[found_empty_clip].fire()
                    self.emulatedLoopClip[str(track_index)] = found_empty_clip
            else:
                self.log.debug("Switch Looper 1")
                track.clip_slots[found_empty_clip].fire()
                self.emulatedLoopClip[str(track_index)] = found_empty_clip

        