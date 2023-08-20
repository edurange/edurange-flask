
import React, { useState } from 'react';
import SampleCard from './SampleCard';

function SampleParent() {

    fakeData = [ { title: "fake1", id: 123} , { title: "fake2", id: 456} , { title: "fake3", id: 789}  ]

    return (
        <>
            {fakeData.map((card) => (
                <div>
                    <SampleCard
                    title = {card.title}
                    id = {card.id}
                    />
                </div>
            ))}
        </>
    )

}
export default SampleParent;

