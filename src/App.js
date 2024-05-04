import React, { useState, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  VStack,
  extendTheme,
  Button,
  FormControl,
  FormLabel,
  Textarea,
  useToast,
  useColorMode,
  IconButton,
  Image,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Progress,
} from '@chakra-ui/react';
import { FaSun, FaMoon } from 'react-icons/fa';
import { Amplify } from 'aws-amplify';
import { uploadData } from 'aws-amplify/storage';
import awsExports from './aws-exports';
import startRecordingSound from './sounds/start-recording.mp3';
import stopRecordingSound from './sounds/stop-recording.mp3';

Amplify.configure(awsExports);

// Custom theme colors
const customTheme = extendTheme({
  initialColorMode: 'light',
  useSystemColorMode: false,
  colors: {
    brand: {
      900: '#1a365d',
      800: '#153e75',
      700: '#2a69ac',
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'bold',
      },
    },
  },
});

function App() {
  const [textData, setTextData] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  // const [audioBlob, setAudioBlob] = useState(null); // Commented out for testing purposes
  const [isPolicyModalOpen, setPolicyModalOpen] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const toast = useToast();
  const { colorMode, toggleColorMode, setColorMode } = useColorMode();

  useEffect(() => {
    const savedColorMode = localStorage.getItem('colorMode');
    if (savedColorMode) {
      setColorMode(savedColorMode);
    }
  }, [setColorMode]);

  const handleToggleColorMode = () => {
    toggleColorMode();
    const newColorMode = colorMode === 'light' ? 'dark' : 'light';
    localStorage.setItem('colorMode', newColorMode);
  };

  const handleTextChange = (e) => setTextData(e.target.value);

  const playSound = (soundFile) => {
    const audio = new Audio(soundFile);
    audio.play();
  };

  const startRecording = async () => {
    // Inform the user about the microphone permission prompt
    toast({
      title: 'Microphone Access',
      description: 'You will be prompted to allow microphone access. Please select "Allow" to start recording.',
      status: 'info',
      duration: 5000,
      isClosable: true,
    });

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);
      recorder.start();
      setIsRecording(true);
      playSound(startRecordingSound); // Play start recording sound
    } catch (error) {
      toast({
        title: 'Error accessing your microphone',
        description: 'Please ensure you have given the necessary permissions.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
      playSound(stopRecordingSound); // Play stop recording sound
    }
  };

  const handleSubmit = async () => {
    if (textData) {
      try {
        // Upload text data as a file
        const textFileName = `textData-${Date.now()}.txt`;
        const textFile = new Blob([textData], { type: 'text/plain' });
        await uploadData({
          path: textFileName,
          data: textFile,
          options: {
            contentType: 'text/plain',
            progressCallback(progress) {
              const uploadPercentage = Math.round((progress.loaded / progress.total) * 100);
              setUploadProgress(uploadPercentage);
            },
          },
        });
        setSubmissionStatus('success');
        // Display a toast on successful submission for user feedback
        toast({
          title: 'Data submitted successfully.',
          description: 'Your text data has been uploaded.',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });

        // Clear the form
        setTextData('');
        setUploadProgress(0); // Reset upload progress after submission
      } catch (error) {
        setSubmissionStatus('error');
        toast({
          title: 'Submission failed.',
          description: 'There was an error uploading your data.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    } else {
      toast({
        title: 'Missing data.',
        description: 'Please provide text data.',
        status: 'warning',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const togglePolicyModal = () => setPolicyModalOpen(!isPolicyModalOpen);

  return (
    <ChakraProvider theme={customTheme}>
      <Box position="relative" textAlign="center" fontSize="xl" minHeight="100vh" py={10}>
        {/* <Image src="lady_cat_7.jpg" alt="Cultural Hut" opacity="0.8" position="absolute" top="0" left="0" width="full" height="full" objectFit="cover" zIndex="-1" /> */}
        <Box position="absolute" bottom="4" right="4" zIndex="2" width="150px" height="auto">
          <Image src="susan_signature.jpg" alt="Susan Ngatia's Signature" opacity="1" />
        </Box>
        <Box bg={colorMode === 'light' ? 'white' : 'brand.800'} color={colorMode === 'light' ? 'brand.800' : 'white'}>
          <VStack spacing={8} maxWidth="xl" mx="auto" p={4}>
            <IconButton icon={colorMode === 'light' ? <FaMoon /> : <FaSun />} isRound="true" size="lg" alignSelf="flex-end" m={4} onClick={handleToggleColorMode} />
            <Text fontSize="3xl" fontWeight="bold">Welcome to the Kikuyu Language Data Collection Interface</Text>
            <Text fontSize="md">
              Please submit text data and voice recordings specifically for the Kikuyu language.
            </Text>
            {submissionStatus === 'success' && (
              <Text fontSize="lg" color="green.500" my={4}>
                Your submission has been successfully received. Thank you!
              </Text>
            )}
            <FormControl id="text-data-form">
              <FormLabel>Text Data</FormLabel>
              <Textarea
                value={textData}
                onChange={handleTextChange}
                placeholder="Enter text data here"
                size="sm"
              />
            </FormControl>
            {isRecording && (
              <Text color="red.500">Recording in progress...</Text>
            )}
            {isRecording ? (
              <Button onClick={stopRecording} colorScheme="red" size="lg">
                Stop Recording
              </Button>
            ) : (
              <Button onClick={startRecording} colorScheme="green" size="lg">
                Start Recording
              </Button>
            )}
            {uploadProgress > 0 && (
              <Progress value={uploadProgress} size="xs" colorScheme="green" />
            )}
            <Button
              onClick={handleSubmit}
              colorScheme="brand"
              size="lg"
              isDisabled={!textData}
            >
              Submit
            </Button>
            <Button onClick={togglePolicyModal} colorScheme="blue" size="sm" mt={4}>
              View Data User Policy and Privacy Policy
            </Button>
            <Modal isOpen={isPolicyModalOpen} onClose={togglePolicyModal}>
              <ModalOverlay />
              <ModalContent>
                <ModalHeader>Data User Policy and Privacy Policy</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                  <Text fontSize="md">
                    The data collected through this interface will be used solely for the purpose of developing and improving language learning models for Kenyan languages. We are committed to maintaining the privacy and security of your submissions.
                  </Text>
                  <Text fontSize="md" mt={4}>
                    By submitting your text and voice recordings, you grant us permission to use the data for research and development purposes. Your submissions will be anonymized and will not be shared with third parties without your explicit consent.
                  </Text>
                </ModalBody>
                <ModalFooter>
                  <Button colorScheme="blue" mr={3} onClick={togglePolicyModal}>
                    Close
                  </Button>
                </ModalFooter>
              </ModalContent>
            </Modal>
          </VStack>
        </Box>
      </Box>
    </ChakraProvider>
  );
}

export default App;
