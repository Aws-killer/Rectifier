import {
	AbsoluteFill,
	Series,
	interpolate,
	spring,
	useCurrentFrame,
} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Img, Easing, Audio} from 'remotion';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import GsapAnimation from './Components/GsapAnimation';
import gsap from 'gsap';
import {MotionPathPlugin} from 'gsap-trial/all';

export default function ImageStream() {
	const {fps} = useVideoConfig();

	return (
		<AbsoluteFill
			style={{
				top: '50%',
				left: '50%',
				transform: 'translate(-50%, -50%)',
				color: 'white',
				position: 'absolute',
				width: '100%',
				height: '100%',
				zIndex: 0,
				objectFit: 'cover',
			}}
		>
			<TransitionSeries>
				{imageSequences.map((entry, index) => {
					return (
						<>
							<TransitionSeries.Sequence
								key={entry.start}
								durationInFrames={fps * (entry.end - entry.start)}
							>
								<Images key={index} index={index} entry={entry} />;
							</TransitionSeries.Sequence>
						</>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
}

const Images = ({entry,index}) => {
	const plugins = [MotionPathPlugin];
	const gsapTimeline = () => {
		let tlContainer = gsap.timeline();
		tlContainer.fromTo(
			'#gaussianBlur',
			{
				attr: {stdDeviation: `250,0`},
			},
			{
				attr: {stdDeviation: `0,0`},

				duration: 1 / 2,
			},
			0
		);
		tlContainer.to('#imagex', {
			duration: 2, // Total duration for one loop
			ease: 'power1.inOut',
			scale: 1.2,
			// motionPath: {
			// 	path: CAMERA_PATHS[index % CAMERA_PATHS.length],
			// 	align: '#imagex',
			// 	alignOrigin: [0.5, 0.5],
			// 	autoRotate: false,
			// },
		});

		return tlContainer;
	};
	return (
		<>
			<GsapAnimation
				plugins={plugins}
				style={{
					BackgroundColor: 'black',
				}}
				className="bg-black"
				Timeline={gsapTimeline}
			>
				<Audio src={staticFile('sfx_1.mp3')} />
				<svg
					xmlns="http://www.w3.org/2000/svg"
					version="1.1"
					className="filters"
				>
					<defs>
						<filter id="blur">
							<feGaussianBlur id="gaussianBlur" in="SourceGraphic" />
						</filter>
					</defs>
				</svg>
				<Img
					id="imagex"
					style={{
						filter: `url(#blur)`,
						objectPosition: 'center',
						objectFit: 'cover',

						position: 'absolute',
						top: '50%', // Center vertically
						left: '50%', // Center horizontally
						transform: 'translate(-50%, -50%)',

						width: 1080,
						height: 1920,
					}}
					src={staticFile(entry.name)}
				/>
			</GsapAnimation>
		</>
	);
};

const CAMERA_PATHS = [
	'M0,0 L0,0 L0.01,6.250767223456442 L0.02,12.307777919193562 L0.03,17.981021128648393 L0.04,23.08791053766677 L0.05,27.456831719591154 L0.06,30.930494499238577 L0.07,33.36903077821196 L0.08,34.65278258690877 L0.09,34.68473051456858 L0.1,33.39251892264521 L0.11,30.730041360606144 L0.12,26.67855725570995 L0.13,21.24731910710591 L0.14,14.473697938680804 L0.15,6.422803507059508 L0.16,-2.813395430132172 L0.17,-13.117436757566923 L0.18,-24.348194042382275 L0.19,-36.34313835339807 L0.2,-48.92099466211533 L0.21,-61.884747703696206 L0.22,-75.02494602649278 L0.23,-88.12324769059636 L0.24,-100.95614678075249 L0.25,-113.29881665150901 L0.26,-124.92900367924119 L0.27,-135.63090429430372 L0.28,-145.19895822488047 L0.29,-153.44149220001046 L0.3,-160.18415081068855 L0.31,-165.27305477318492 L0.32,-168.57763141725664 L0.33,-169.99306775534885 L0.34,-169.44234288234307 L0.35000000000000003,-166.87780359918514 L0.36,-162.28225492514437 L0.37,-155.6695454289916 L0.38,-147.08463592697137 L0.39,-136.60314891690805 L0.4,-124.33040499141937 L0.41000000000000003,-110.39996124635968 L0.42,-94.97167522233873 L0.43,-78.22932604080408 L0.44,-60.37783198193181 L0.45,-41.64011066884246 L0.46,-22.253634152367002 L0.47000000000000003,-2.4667364271843444 L0.48,17.465264836574214 L0.49,37.28406736544427 L0.5,56.73243709264525 L0.51,75.55824670277104 L0.52,93.51843213440384 L0.53,110.38280065041089 L0.54,125.93762660845078 L0.55,139.98897467993305 L0.56,152.36569491216275 L0.5700000000000001,162.92203962582144 L0.58,171.53985859202433 L0.59,178.1303361290115 L0.6,182.63524157436322 L0.61,185.02767289005592 L0.62,185.3122818019912 L0.63,183.5249777141914 L0.64,179.7321165187357 L0.65,174.02918919305938 L0.66,166.5390335857308 L0.67,157.40960089406326 L0.68,146.81131589274514 L0.6900000000000001,134.93407685237096 L0.7000000000000001,121.98394717226348 L0.71,108.1795959389706 L0.72,93.74854882143232 L0.73,78.92331385425543 L0.74,63.937448688246285 L0.75,49.02163676798019 L0.76,34.3998396151561 L0.77,20.2855909592305 L0.78,6.878495888722427 L0.79,-5.639005457500526 L0.8,-17.104554816151857 L0.81,-27.378424117590406 L0.8200000000000001,-36.34565243250325 L0.8300000000000001,-43.91773597715466 L0.84,-50.03384340800965 L0.85,-54.66153690980771 L0.86,-57.79698818378553 L0.87,-59.464687225962315 L0.88,-59.7166505974229 L0.89,-58.631144577076576 L0.9,-56.310947002332334 L0.91,-52.881179599165826 L0.92,-48.486750042076004 L0.93,-43.28944973799401 L0.9400000000000001,-37.46475927975189 L0.9500000000000001,-31.19841856151882 L0.96,-24.682822603635902 L0.97,-18.113307127579862 L0.98,-11.684389801835987 L0.99,-5.586033813903673',

	'M0,0 C0,0 0,100 0,0 C9.983341664682815,0 0,99.50041652780259 0,0 C19.866933079506122,0 0,98.00665778412416 0,0 C29.55202066613396,0 0,95.5336489125606 0,0 C38.941834230865055,0 0,92.10609940028851 0,0 C47.942553860420304,0 0,87.75825618903727 0,0 C56.46424733950355,0 0,82.53356149096783 0,0 C64.42176872376912,0 0,76.48421872844884 0,0 C71.73560908995228,0 0,69.67067093471654 0,0 C78.33269096274834,0 0,62.16099682706644 0,0 C84.14709848078965,0 0,54.03023058681398 0,0 C89.12073600614355,0 0,45.35961214255773 0,0 C93.20390859672264,0 0,36.235775447667336 0,0 C96.3558185417193,0 0,26.749882862458733 0,0 C98.54497299884602,0 0,16.99671429002408 0,0 C99.74949866040545,0 0,7.073720166770291 0,0 C99.95736030415051,0 0,-2.9199522301288816 0,0 C99.16648104524685,0 0,-12.884449429552486 0,0 C97.38476308781952,0 0,-22.72020946930871 0,0 C94.63000876874145,0 0,-32.32895668635036 0,0 C90.92974268256818,0 0,-41.61468365471424 0,0 C86.32093666488737,0 0,-50.48461045998576 0,0 C80.849640381959,0 0,-58.85011172553458 0,0 C74.57052121767201,0 0,-66.62760212798244 0,0 C67.54631805511507,0 0,-73.73937155412457 0,0 C59.84721441039566,0 0,-80.11436155469337 0,0 C51.550137182146415,0 0,-85.68887533689474 0,0 C42.737988023382975,0 0,-90.40721420170613 0,0 C33.498815015590466,0 0,-94.22223406686582 0,0 C23.9249329213982,0 0,-97.09581651495907 0,0 C14.112000805986721,0 0,-98.99924966004454 0,0 C4.158066243329049,0 0,-99.91351502732795 0,0 C-5.8374143427580085,0 0,-99.82947757947531 0,0 C-15.774569414324866,0 0,-98.74797699088649 0,0 C-25.554110202683166,0 0,-96.6798192579461 0,0 C-35.07832276896198,0 0,-93.64566872907963 0,0 C-44.252044329485244,0 0,-89.6758416334147 0,0 C-52.98361409084934,0 0,-84.8100031710408 0,0 C-61.185789094271925,0 0,-79.09677119144165 0,0 C-68.77661591839741,0 0,-72.59323042001398 0,0 C-75.68024953079282,0 0,-65.3643620863612 0,0 C-81.82771110644109,0 0,-57.48239465332685 0,0 C-87.15757724135882,0 0,-49.026082134069945 0,0 C-91.61659367494549,0 0,-40.079917207997546 0,0 C-95.1602073889516,0 0,-30.733286997841937 0,0 C-97.7530117665097,0 0,-21.07957994307797 0,0 C-99.36910036334645,0 0,-11.215252693505398 0,0 C-99.99232575641008,0 0,-1.2388663462890561 0,0 C-99.61646088358405,0 0,8.749898343944727 0,0 C-98.24526126243325,0 0,18.651236942257576 0,0 C-95.89242746631385,0 0,28.366218546322624 0,0 C-92.58146823277322,0 0,37.79777427129811 0,0 C-88.34546557201531,0 0,46.85166713003771 0,0 C-83.22674422239008,0 0,55.437433617916156 0,0 C-77.27644875559872,0 0,63.46928759426347 0,0 C-70.55403255703919,0 0,70.866977429126 0,0 C-63.12666378723208,0 0,77.55658785102501 0,0 C-55.06855425976376,0 0,83.47127848391598 0,0 C-46.46021794137566,0 0,88.55195169413193 0,0 C-37.3876664830236,0 0,92.74784307440359 0,0 C-27.941549819892586,0 0,96.01702866503659 0,0 C-18.216250427209502,0 0,98.32684384425848 0,0 C-8.30894028174964,0 0,99.65420970232175 0,0 C1.6813900484350601,0 0,99.98586363834151 0,0 C11.654920485049363,0 0,99.31849187581926 0,0 C21.511998808781552,0 0,97.65876257280235 0,0 C31.15413635133787,0 0,95.02325919585293 0,0 C40.48499206165983,0 0,91.43831482353194 0,0 C49.41133511386089,0 0,86.93974903498248 0,0 C57.84397643882001,0 0,81.57251001253569 0,0 C65.6986598718789,0 0,75.39022543433046 0,0 C72.89690401258765,0 0,68.45466664428059 0,0 C79.36678638491532,0 0,60.83513145322546 0,0 C85.04366206285648,0 0,52.60775173811045 0,0 C89.87080958116269,0 0,43.85473275743904 0,0 C93.7999976774739,0 0,34.663531783502584 0,0 C96.79196720314866,0 0,25.125984258225486 0,0 C98.81682338770004,0 0,15.337386203786435 0,0 C99.8543345374605,0 0,5.395542056264886 0,0 C99.8941341839772,0 0,-4.600212563953695 0,0 C98.93582466233818,0 0,-14.550003380861353 0,0 C96.98898108450862,0 0,-24.354415373579112 0,0 C94.07305566797726,0 0,-33.915486098383624 0,0 C90.21718337562933,0 0,-43.13768449706208 0,0 C85.45989080882805,0 0,-51.92886541166855 0,0 C79.84871126234903,0 0,-60.201190268482364 0,0 C73.43970978741133,0 0,-67.87200473200124 0,0 C66.2969230082182,0 0,-74.86466455973999 0,0 C58.49171928917617,0 0,-81.1093014061656 0,0 C50.10208564578846,0 0,-86.54352092411123 0,0 C41.21184852417566,0 0,-91.1130261884677 0,0 C31.909836234935213,0 0,-94.77216021311119 0,0 C22.288991410024593,0 0,-97.48436214041641 0,0 C12.44544235070617,0 0,-99.22253254526035 0,0 C2.4775425453357767,0 0,-99.96930420352065 0,0 C-7.51511204618093,0 0,-99.71721561963784 0,0 C-17.43267812229814,0 0,-98.46878557941267 0,0 C-27.17606264109442,0 0,-96.23648798313097 0,0 C-36.64791292519284,0 0,-93.04262721047533 0,0 C-45.75358937753214,0 0,-88.91911526253608 0,0',
	'M0,0 L100,0 L99.51036656945537,9.984339998849284 L98.02625911568099,19.870906466122022 L95.56230900723436,29.5608862723338 L92.14294184004864,38.957410964557404 L87.80213531713179,47.96652513735051 L82.5830816278624,56.49812588790725 L76.53775768155874,64.46686396187575 L69.72640747146431,71.79299757722424 L62.2169417242108,78.40319038461482 L54.08426081740079,84.23124557927044 L45.40950771591454,89.2187688157503 L36.279258378204545,93.31575328703872 L26.78465771017993,96.48108110582352 L17.020509690030114,98.68293596104441 L7.084330747020447,99.89912290839605 L-2.9246241536970876,100.11729208063714 L-12.906352993582725,99.33506406302378 L-22.76110584635347,97.5600556613776 L-32.39038170405442,94.80980578540205 L-41.69791302202367,91.11160216793331 L-50.590628141951726,86.50221063188363 L-58.97958197133076,81.02750959079931 L-66.7808456128768,74.74203341647265 L-73.91634604585447,67.70842921844734 L-80.3146474585801,59.99683244642164 L-85.91166641277066,51.68416753882 L-90.65131368005072,42.85338059104611 L-94.48605632225305,33.59261169763412 L-97.37739438285246,23.994315226870256 L-99.29624740902467,14.15433680840468 L-100.22324692391267,4.170956248683369 L-100.14893190772963,-5.8560940686548335 L-99.07384531495642,-15.826625493392138 L-97.0085306434231,-25.640994177372292 L-93.97342856963141,-35.20109689865335 L-89.99867466329499,-44.411351689071395 L-85.12380018277366,-53.179653462985485 L-79.39733892196912,-61.41829509283016 L-72.87634401865205,-69.04484472047916 L-65.62581953470664,-75.982970528916 L-57.71807247140549,-82.1632047219775 L-49.23199167903304,-87.52363906577253 L-40.252260851991934,-92.01054502774777 L-30.86851346063244,-95.57891230146299 L-21.17443805282182,-98.192900319459 L-11.266842855895522,-99.82619822501783 L-1.2446890181166146,-100.46228968746522 L8.791897855995662,-100.09461989582526 L18.74262800327464,-98.72666304261917 L28.50804963905424,-96.37188960364541 L37.99054292008173,-93.05363372076036 L47.095295799113906,-88.80486199298979 L55.73125201609111,-83.66784596676875 L63.812021747272496,-77.69374157887896 L71.2567458049862,-70.94207973610291 L77.99090474299076,-63.48017310444059 L83.9470647712743,-55.382445019044404 L89.0655530139579,-46.72968720543564 L93.29505534854258,-37.60825371527344 L96.5931308370268,-28.10919911881194 L98.92663759170844,-18.32736955481548 L100.27206580247615,-8.360455711496488 L100.61577457926306,1.6919828057402009 L99.9541302238245,11.72951197615368 L98.29354452952558,21.651826801038634 L95.65041270654555,31.359753651256696 L92.05095153284961,40.756241508472954 L87.53093932842037,49.74733219263515 L82.13536033162218,58.24309987624787 L75.91795701237078,66.15855049098207 L68.94069477745498,73.41447203107701 L61.273144399688675,79.9382272468867 L52.99178832579866,85.66448079591534 L44.17925777984408,90.53585357206329 L34.92350827187885,94.50349766005495 L25.316941738588003,97.52758615389259 L15.45548407755559,99.57771292778533 L5.437627284303752,100.6331983468527 L-4.63655424320893,100.68329784403063 L-14.666403407908245,99.72731125963688 L-24.5516861381051,97.77459183129315 L-34.193593084390365,94.84445472445466 L-43.49572727838769,90.96598599764705 L-52.36506788112658,86.1777538916222 L-60.712900385764456,80.52742530807899 L-68.45570397269645,74.07129129158307 L-75.51598714140974,66.8737062383897 L-81.82306325853986,59.006446418920916 L-87.31375826033582,50.54799420803598 L-91.93304342416391,41.58275516089324 L-95.6345868710505,32.20021574467312 L-98.38121827210824,22.49405013099682 L-100.14530209793128,12.561184964567738 L-100.90901566303374,2.500831445261933 L-100.6645291680244,-7.586505610619649 L-99.41408592097503,-17.6000318322722 L-97.16998191656734,-27.439670448713034 L-93.954444957138,-37.00706247185973 L-89.79941450363519,-46.2065499123697',
];
