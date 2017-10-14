//
// Copyright 2016 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
import UIKit
import AVFoundation
import googleapis

let SAMPLE_RATE = 16000
var final_processed_string = ""
extension String {
    func index(of string: String, options: CompareOptions = .literal) -> Index? {
        return range(of: string, options: options)?.lowerBound
    }
    func endIndex(of string: String, options: CompareOptions = .literal) -> Index? {
        return range(of: string, options: options)?.upperBound
    }
    func indexes(of string: String, options: CompareOptions = .literal) -> [Index] {
        var result: [Index] = []
        var start = startIndex
        while let range = range(of: string, options: options, range: start..<endIndex) {
            result.append(range.lowerBound)
            start = range.upperBound
        }
        return result
    }
    func ranges(of string: String, options: CompareOptions = .literal) -> [Range<Index>] {
        var result: [Range<Index>] = []
        var start = startIndex
        while let range = range(of: string, options: options, range: start..<endIndex) {
            result.append(range)
            start = range.upperBound
        }
        return result
    }
}
class ViewController : UIViewController, AudioControllerDelegate {
    
  @IBOutlet weak var textView: UITextView!
    
    @IBOutlet weak var AccuracyLabel1: UILabel!
    @IBOutlet weak var AccuracyLabel2: UILabel!
    @IBOutlet weak var original_text: UITextView!
    var audioData: NSMutableData!
    var audio_processed = [String]()
    var audioRecorder: AVAudioRecorder?
  override func viewDidLoad() {
    super.viewDidLoad()
    AudioController.sharedInstance.delegate = self
    let fileMgr = FileManager.default
    
    let dirPaths = fileMgr.urls(for: .documentDirectory,
                                in: .userDomainMask)
    
    let soundFileURL = dirPaths[0].appendingPathComponent("sound.caf")
    print(soundFileURL)
    
    let recordSettings =
        [AVEncoderAudioQualityKey: AVAudioQuality.min.rawValue,
         AVEncoderBitRateKey: 16,
         AVNumberOfChannelsKey: 2,
         AVSampleRateKey: 44100.0] as [String : Any]
    
    let audioSession = AVAudioSession.sharedInstance()
    do {
        try audioSession.setCategory(
            AVAudioSessionCategoryPlayAndRecord)
    } catch let error as NSError {
        print("audioSession error: \(error.localizedDescription)")
    }
    
    do {
        try audioRecorder = AVAudioRecorder(url: soundFileURL,
                                            settings: recordSettings as [String : AnyObject])
        audioRecorder?.prepareToRecord()
    } catch let error as NSError {
        print("audioSession error: \(error.localizedDescription)")
    }
  }

    @IBAction func start_processing(_ sender: Any) {
        self.view.endEditing(true)
    }
    @IBAction func recordAudio(_ sender: NSObject) {
    let audioSession = AVAudioSession.sharedInstance()
    do {
      try audioSession.setCategory(AVAudioSessionCategoryRecord)
    } catch {

    }
    audioData = NSMutableData()
    _ = AudioController.sharedInstance.prepare(specifiedSampleRate: SAMPLE_RATE)
    SpeechRecognitionService.sharedInstance.sampleRate = SAMPLE_RATE
    _ = AudioController.sharedInstance.start()
    audioRecorder?.record()
  }

  @IBAction func stopAudio(_ sender: NSObject) {
    _ = AudioController.sharedInstance.stop()
    SpeechRecognitionService.sharedInstance.stopStreaming()
    for element in audio_processed
    {
        print(element)
    }
    audioRecorder?.stop()
    print(final_processed_string)
    let dict = ["actualText": "Hi my name is John and I like icecream.", "recitedText": final_processed_string] as [String: Any]
    
    if let jsonData = try? JSONSerialization.data(withJSONObject: dict, options: .prettyPrinted) {
        
        let url = NSURL(string: "https://snappy-frame-171902.appspot.com/getAccuracies")!
        let request = NSMutableURLRequest(url: url as URL)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        let task = URLSession.shared.dataTask(with: request as URLRequest){ data,response,error in
            if error != nil{
                print(error?.localizedDescription)
                return
            }
            
            do {
                let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary
                
                if let parseJSON = json {
                    let resultValue:String = parseJSON["success"] as! String;
                    print("result: \(resultValue)")
                    print(parseJSON)
                }
            } catch let error as NSError {
                print(error)
            }
        }
        task.resume()
    }
//    let json: [String: Any] = ["actualText": "Hi my name is John and I like icecream.",
//                               "recitedText": final_processed_string]
//
//    let jsonData = try? JSONSerialization.data(withJSONObject: json)
//
//    // create post request
//    let url = URL(string: "https://snappy-frame-171902.appspot.com/getAccuracies")!
//    var request = URLRequest(url: url)
//    request.httpMethod = "POST"
//
//    // insert json data to the request
//    request.addValue("application/json", forHTTPHeaderField: "Content-Type")
//    request.httpBody = jsonData
//    let task = URLSession.shared.dataTask(with: request) { data, response, error in
//        guard let data = data, error == nil else {
//            print(error?.localizedDescription ?? "No data")
//            return
//        }
//        let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
//        print(JSONSerialization.isValidJSONObject(data))
////        print(type(of: data))
////        print(data)
////        print(responseJSON)
//        if let dict = responseJSON as? [String: Any]{
//            self.AccuracyLabel1.text = String(describing: dict["Rishis method"])
//            self.AccuracyLabel2.text = String(describing: dict["Twin Words"])
//            print(dict["Rishis method"])
//            print(dict["Twin Words"])
//        }
//    }
//
//    task.resume()
  }

  func processSampleData(_ data: Data) -> Void {
    audioData.append(data)
    // We recommend sending samples in 100ms chunks
    let chunkSize : Int /* bytes/chunk */ = Int(0.1 /* seconds/chunk */
      * Double(SAMPLE_RATE) /* samples/second */
      * 2 /* bytes/sample */);

    if (audioData.length > chunkSize) {
      SpeechRecognitionService.sharedInstance.streamAudioData(audioData,
                                                              completion:
        { [weak self] (response, error) in
            guard let strongSelf = self else {
                return
            }
            
            if let error = error {
                strongSelf.textView.text = error.localizedDescription
            } else if let response = response {
                var finished = false
                print(response)
                for result in response.resultsArray! {
                    if let result = result as? StreamingRecognitionResult {
                        if result.isFinal {
                            finished = true
                            let stringedresult = String(describing: result)
                            let stringedresult2 = stringedresult.substring(from: stringedresult.endIndex(of: "transcript: \"")!)
                            print(stringedresult2)
                            let finalstringedresult = stringedresult2.substring(to: stringedresult2.index(of: "\"")!)
                            self?.audio_processed.append(finalstringedresult)                        }
                    }
                }
                var printingstring = ""
                for element in (self?.audio_processed)!
                {
                    printingstring = printingstring + "" + element
                }
                strongSelf.textView.text = printingstring
                if finished {
                    //strongSelf.stopAudio(strongSelf)
                    final_processed_string = printingstring
                    
                }
            }
      })
      self.audioData = NSMutableData()
    }
  }
}
