import React, { useState, useEffect, useRef } from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  VStack,
  extendTheme,
  Button,
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
  Textarea,
  Flex,
  Heading,
  Stack,
  Link,
} from '@chakra-ui/react';
import { FaSun, FaMoon, FaHandshake } from 'react-icons/fa';
import { Amplify } from 'aws-amplify';
import { uploadData } from 'aws-amplify/storage';
import awsExports from './aws-exports';
import startRecordingSound from './sounds/start-recording.mp3';
import stopRecordingSound from './sounds/stop-recording.mp3';
import DataInsights from './DataInsights';
import PartnershipPackages from './PartnershipPackages';
import * as tf from '@tensorflow/tfjs';

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
  // The 'isRecording' state is used to track whether the user is currently recording audio
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  // const [audioBlob, setAudioBlob] = useState(null); // Commented out for testing purposes
  const [isPolicyModalOpen, setPolicyModalOpen] = useState(false);
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [currentView, setCurrentView] = useState('dataCollection');
  const toast = useToast();
  const { colorMode, toggleColorMode, setColorMode } = useColorMode();
  const dataCollectionRef = useRef(null);
  const dataInsightsRef = useRef(null);
  const partnershipPackagesRef = useRef(null);

  useEffect(() => {
    const savedColorMode = localStorage.getItem('colorMode');
    if (savedColorMode) {
      setColorMode(savedColorMode);
    }
  }, [setColorMode]);

  useEffect(() => {
    console.log("isRecording state updated to:", isRecording);
  }, [isRecording]);

  const handleToggleColorMode = () => {
    if (toggleColorMode) {
      toggleColorMode();
      const newColorMode = colorMode === 'light' ? 'dark' : 'light';
      localStorage.setItem('colorMode', newColorMode);
    } else {
      console.error('toggleColorMode function is not available');
    }
  };

  const playSound = (soundFile) => {
    const audio = new Audio(soundFile);
    audio.play();
  };

  const startRecording = async () => {
    console.log("Before starting, isRecording:", isRecording); // Log before state change
    console.log("Attempting to start recording and setting isRecording to true...");
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

  const stopRecording = async () => {
      if (mediaRecorder) {
          mediaRecorder.stop();
          console.log("Before stopping, isRecording should be true, checking actual state:", isRecording); // Log before state change
          setIsRecording(false);
          playSound(stopRecordingSound); // Play stop recording sound

          // Handle the recorded audio data
          mediaRecorder.ondataavailable = async (event) => {
              const audioBlob = event.data;
              const arrayBuffer = await audioBlob.arrayBuffer();
              const audioTensor = tf.tensor(new Float32Array(arrayBuffer));

              try {
                  // Load the pre-trained TensorFlow.js model
                  const model = await tf.loadLayersModel('TTS/tts/models/xtts_model.pth');

                  // Perform model inference
                  const modelOutput = model.predict(audioTensor);

                  // Placeholder: Convert the model's output into audible voice-over
                  // This may involve additional processing steps or the use of another library or API
                  console.log("Model output:", modelOutput);
                  // TODO: Implement the logic to generate voice-over from modelOutput

              } catch (error) {
                  console.error("Error during model inference:", error);
              }
          };
      }
  };

  const handleSubmit = async () => {
    if (textData) {
      try {
        const textFileName = `textData-${Date.now()}.txt`;
        const textFile = new Blob([textData], { type: 'text/plain' });
        await uploadData({
          path: textFileName,
          data: textFile,
          options: {
            contentType: 'text/plain',
            progressCallback(progress) {
              // Display a toast on successful submission for user feedback
              toast({
                title: 'Uploading...',
                description: `Your text data is being uploaded. Progress: ${Math.round((progress.loaded / progress.total) * 100)}%`,
                status: 'info',
                duration: 5000,
                isClosable: true,
              });
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

        setTextData('');
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

  const handleStripePayment = async () => {
    try {
        const axios = await import('axios');
        const response = await axios.post('/create-payment-intent', {
            amount: 5000, // Amount in cents (e.g., $50.00)
            currency: 'usd',
        });
        const { paymentIntentId } = response.data;
        toast({
            title: 'Payment Successful',
            description: `Stripe Payment Intent ID: ${paymentIntentId}`,
            status: 'success',
            duration: 5000,
            isClosable: true,
        });
    } catch (error) {
        console.error('Error creating Stripe payment intent:', error);
        toast({
            title: 'Payment Failed',
            description: 'There was an error processing your payment with Stripe.',
            status: 'error',
            duration: 5000,
            isClosable: true,
        });
    }
};

const handlePayPalPayment = async () => {
    try {
        const axios = await import('axios');
        const response = await axios.post('/create-paypal-transaction', {
            amount: '50.00', // Amount in USD
            currency: 'USD',
        });
        const { orderId } = response.data;
        toast({
            title: 'Payment Successful',
            description: `PayPal Order ID: ${orderId}`,
            status: 'success',
            duration: 5000,
            isClosable: true,
        });
    } catch (error) {
        console.error('Error creating PayPal transaction:', error);
        toast({
            title: 'Payment Failed',
            description: 'There was an error processing your payment with PayPal.',
            status: 'error',
            duration: 5000,
            isClosable: true,
        });
    }
};

// Function to change view
const changeView = (view) => {
    setCurrentView(view);
    // Assuming each view has a corresponding ref like dataCollectionRef, dataInsightsRef, etc.
    const viewRef = {
        dataCollection: dataCollectionRef,
        dataInsights: dataInsightsRef,
        partnershipPackages: partnershipPackagesRef,
    }[view];

    if (viewRef && viewRef.current) {
        viewRef.current.scrollIntoView({ behavior: 'smooth' });
    }
};

// Conditional rendering based on current view
let contentView;
switch (currentView) {
    case 'partnershipPackages':
        contentView = <PartnershipPackages />;
        break;
    default:
        contentView = (
            <>
                <DataInsights />
                <Button
                    as="a"
                    href="https://forms.gle/g2WKYZsUXtFhBP3v5" // Updated Google Form link
                    target="_blank"
                    colorScheme="teal"
                    leftIcon={<FaHandshake />}
                    size="lg"
                    mt={4}
                >
                    Partner with Us
                </Button>
                <Textarea
                    placeholder="Enter your text data here..."
                    value={textData}
                    onChange={(e) => setTextData(e.target.value)}
                    size="sm"
                    mt={4}
                />
                <Button
                    onClick={startRecording}
                    colorScheme={isRecording ? "gray" : "green"}
                    size="md"
                    mt={4}
                    isDisabled={isRecording}
                >
                    Start Recording
                </Button>
                <Button
                    onClick={stopRecording}
                    colorScheme={isRecording ? "red" : "gray"}
                    size="md"
                    mt={4}
                    isDisabled={!isRecording}
                    aria-label="Stop Recording"
                >
                    Stop Recording
                </Button>
                <Button
                    onClick={handleSubmit}
                    colorScheme="blue"
                    size="md"
                    mt={4}
                >
                    Submit Text Data
                </Button>
                <Button
                    onClick={handleStripePayment}
                    colorScheme="blue"
                    size="md"
                    mt={4}
                >
                    Pay with Stripe
                </Button>
                <Button
                    onClick={handlePayPalPayment}
                    colorScheme="blue"
                    size="md"
                    mt={4}
                >
                    Pay with PayPal
                </Button>
                <Button
                    onClick={() => changeView('partnershipPackages')}
                    colorScheme="blue"
                    size="md"
                    mt={4}
                >
                    View Partnership Packages
                </Button>
            </>
        );
}

  const togglePolicyModal = () => setPolicyModalOpen(!isPolicyModalOpen);

  return (
    <ChakraProvider theme={customTheme}>
      <Box position="relative" textAlign="center" fontSize="xl" minHeight="100vh" py={10}>
        <Box position="absolute" bottom="4" right="4" zIndex="2" width="150px" height="auto">
          <Image src="susan_signature.jpg" alt="Susan Ngatia's Signature" opacity="1" />
        </Box>
        <Box bg={colorMode === 'light' ? 'white' : 'brand.800'} color={colorMode === 'light' ? 'brand.800' : 'white'}>
          <VStack spacing={8} maxWidth="xl" mx="auto" p={4}>
            <Flex as="header" width="full" align="center" justify="space-between" p={4} bg="blue.500" color="white" position="sticky" top="0" zIndex="3">
              <Heading as="h1" size="lg">codekiijiji.ai</Heading>
              <Stack as="nav" direction="row" spacing={4}>
                <Link href="#data-collection" onClick={() => changeView('dataCollection')} style={{ textDecoration: currentView === 'dataCollection' ? 'underline' : 'none' }}>Data Collection</Link>
                <Link href="#data-insights" onClick={() => changeView('dataInsights')} style={{ textDecoration: currentView === 'dataInsights' ? 'underline' : 'none' }}>Data Insights</Link>
                <Link href="#partnership-packages" onClick={() => changeView('partnershipPackages')} style={{ textDecoration: currentView === 'partnershipPackages' ? 'underline' : 'none' }}>Partnership Packages</Link>
              </Stack>
            </Flex>
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
            <div ref={dataCollectionRef} id="data-collection" devin-id="data-collection">
              {/* Data Collection Section Content */}
            </div>
            <div ref={dataInsightsRef} id="data-insights" devin-id="data-insights">
              {/* Data Insights Section Content */}
            </div>
            <div ref={partnershipPackagesRef} id="partnership-packages" devin-id="partnership-packages">
              {/* Partnership Packages Section Content */}
            </div>
            {contentView}
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
